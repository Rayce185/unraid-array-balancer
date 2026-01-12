# Safety Features

This document explains the safety mechanisms in unRAID Array Balancer.

## Core Principles

1. **Dry Run Default** - All operations preview-only until explicitly enabled
2. **Checksum Verification** - Files verified before source deletion
3. **Safe Checkpoints** - Operations only cancellable at safe points
4. **Mover Awareness** - Pauses when unRAID mover is running
5. **Undo Capability** - Reverse completed moves within 24 hours

## Protection Layers

### Layer 1: Read-Only Start

When first installed, the application:
- Can only read and display disk information
- Cannot move any files
- `DRY_RUN=true` by default

To enable actual moves, you must explicitly set `DRY_RUN=false`.

### Layer 2: Permission Verification

On startup, the application checks:
- Read access to all disks
- Write access to all disks
- Access to share configurations
- Ability to read mover status

If permissions fail:
- Critical failures prevent operation
- Warnings are displayed prominently
- User can choose to continue with limited functionality

### Layer 3: Pre-Operation Checks

Before every file move:
- Source file exists and is readable
- Source directory is writable (for deletion)
- Destination directory exists and is writable
- Destination has sufficient space
- File is not locked by another process
- Share rules allow the destination

### Layer 4: Checksum Verification

For every file move:
1. Calculate checksum of source file
2. Copy file to destination
3. Calculate checksum of destination file
4. Compare checksums
5. **Only delete source if checksums match**

If checksum fails:
- Source file is NOT deleted
- Partial destination file is removed
- Task is marked as failed
- User is alerted

### Layer 5: Mover Awareness

The application:
- Checks for `/var/run/mover.pid` before operations
- Automatically pauses if mover starts
- Resumes after mover completes
- Warns if mover is scheduled soon

### Layer 6: Safe Cancellation

Operations can only be cancelled at safe points:
- Between files in a batch
- After a file is fully copied but before verification
- Never during active file transfer

Cancellation process:
1. User requests cancel
2. System waits for safe point (shows countdown)
3. Cleans up any partial files
4. Records task as cancelled (with redo option)

### Layer 7: Undo Capability

For 24 hours after a move:
- Undo record is kept in database
- User can reverse the operation
- System verifies space and checks for conflicts
- Undo operation uses same safety checks

## What We Never Do

1. **Never delete source without verification** - Checksum must match
2. **Never run during mover** - Always pause and wait
3. **Never force cancel** - Always wait for safe point
4. **Never ignore permission errors** - Either fail or skip
5. **Never modify system files** - Only array disks
6. **Never use shell commands** - All operations via Python APIs

## Logging

All operations are logged:
- `/app/data/logs/array-balancer.log` - Main log
- `/app/data/logs/operations.log` - Audit trail

Log retention: 90 days (configurable)

## Recovery

If something goes wrong:

### Container Crashes During Move
1. Check undo log for incomplete operations
2. Partial files are automatically cleaned on restart
3. Review logs for what was in progress

### Checksum Mismatch
1. Source file is preserved
2. Destination partial is deleted
3. Task fails with error
4. User investigates cause

### Permission Error Mid-Operation
1. Current file is skipped
2. Task pauses with alert
3. User can fix permissions and retry
4. Or skip and continue with remaining files

## Testing Your Setup

Before running on production data:

1. **Create test directories**
   ```
   mkdir /mnt/disk1/test-balance
   mkdir /mnt/disk2/test-balance
   ```

2. **Create test files**
   ```
   dd if=/dev/urandom of=/mnt/disk1/test-balance/test1.bin bs=1M count=100
   ```

3. **Run balance on test data only**

4. **Verify files moved correctly**

5. **Test undo functionality**

6. **Only then** use on real data

## Emergency Stop

If you need to stop immediately:
1. Click "Pause" in the UI
2. Or stop the container: `docker stop array-balancer`
3. Review logs
4. Partial files will be cleaned on restart
