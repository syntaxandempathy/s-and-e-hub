#!/usr/bin/env python3
"""
Image Compression Tool for Syntax & Empathy Project

This tool compresses PNG and JPEG images to reduce repository size while
maintaining visual quality. Designed for batch processing of article images.

Usage:
    python compress_images.py [--directory PATH] [--quality 80] [--size-threshold 1]

Example:
    python compress_images.py --directory ../articles --quality 85 --size-threshold 2
"""

import argparse
from pathlib import Path
from PIL import Image
import sys


def compress_image(input_path: Path, quality: int = 85, max_size_mb: float = 2.0) -> dict:
    """
    Compress a single image file.

    Args:
        input_path: Path to the input image
        quality: JPEG quality (1-100, higher = better quality)
        max_size_mb: Maximum size threshold in MB

    Returns:
        Dict with compression results
    """
    try:
        original_size = input_path.stat().st_size
        original_size_mb = original_size / (1024 * 1024)

        # Skip if already small enough
        if original_size_mb <= max_size_mb:
            return {
                'status': 'skipped',
                'reason': f'Already {original_size_mb:.1f}MB (under {max_size_mb}MB threshold)',
                'original_size_mb': original_size_mb,
                'final_size_mb': original_size_mb,
                'savings_percent': 0
            }

        with Image.open(input_path) as img:
            # Create backup name
            backup_path = input_path.with_suffix(f'.original{input_path.suffix}')

            # Backup original if it doesn't exist
            if not backup_path.exists():
                input_path.rename(backup_path)

            # Determine output format and settings
            if input_path.suffix.lower() in ['.png']:
                if img.mode == 'RGBA':
                    # Keep PNG for transparency
                    img.save(input_path, 'PNG', optimize=True, compress_level=6)
                else:
                    # Convert to JPEG for better compression
                    rgb_img = img.convert('RGB')
                    jpeg_path = input_path.with_suffix('.jpg')
                    rgb_img.save(jpeg_path, 'JPEG', quality=quality, optimize=True)
                    # Remove original PNG
                    input_path.unlink()
                    # Update path reference
                    input_path = jpeg_path
            else:
                # JPEG optimization
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(input_path, 'JPEG', quality=quality, optimize=True)

        final_size = input_path.stat().st_size
        final_size_mb = final_size / (1024 * 1024)
        savings_percent = ((original_size - final_size) / original_size) * 100

        return {
            'status': 'compressed',
            'original_size_mb': original_size_mb,
            'final_size_mb': final_size_mb,
            'savings_percent': savings_percent,
            'backup_created': backup_path.name
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


def find_large_images(directory: Path, size_threshold_mb: float = 1.0) -> list:
    """Find images larger than the size threshold."""
    large_images = []

    for pattern in ['*.png', '*.jpg', '*.jpeg']:
        for img_path in directory.rglob(pattern):
            size_mb = img_path.stat().st_size / (1024 * 1024)
            if size_mb > size_threshold_mb:
                large_images.append((img_path, size_mb))

    # Sort by size (largest first)
    large_images.sort(key=lambda x: x[1], reverse=True)
    return large_images


def main():
    parser = argparse.ArgumentParser(description='Compress large images in the project')
    parser.add_argument('--directory', '-d', type=Path, default='../articles',
                        help='Directory to search for images (default: ../articles)')
    parser.add_argument('--quality', '-q', type=int, default=85,
                        help='JPEG quality 1-100 (default: 85)')
    parser.add_argument('--size-threshold', '-s', type=float, default=1.0,
                        help='Size threshold in MB (default: 1.0)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be compressed without doing it')

    args = parser.parse_args()

    if not args.directory.exists():
        print(f"Error: Directory {args.directory} does not exist")
        sys.exit(1)

    print(f"🔍 Scanning for images larger than {args.size_threshold}MB in {args.directory}")
    large_images = find_large_images(args.directory, args.size_threshold)

    if not large_images:
        print("✅ No large images found!")
        return

    print(f"\n📊 Found {len(large_images)} large images:")
    total_size_mb = 0

    for img_path, size_mb in large_images:
        print(f"  • {img_path.relative_to(args.directory)} ({size_mb:.1f}MB)")
        total_size_mb += size_mb

    print(f"\n💾 Total size: {total_size_mb:.1f}MB")

    if args.dry_run:
        print("\n🔍 Dry run mode - no files will be modified")
        return

    # Ask for confirmation
    response = input(f"\n🤔 Compress {len(large_images)} images? (y/N): ")
    if response.lower() != 'y':
        print("❌ Cancelled")
        return

    print(f"\n🗜️  Compressing images with quality={args.quality}...")

    total_savings_mb = 0
    successful_compressions = 0

    for img_path, original_size_mb in large_images:
        print(f"Processing {img_path.name}...", end=' ')

        result = compress_image(img_path, quality=args.quality, max_size_mb=args.size_threshold)

        if result['status'] == 'compressed':
            savings_mb = result['original_size_mb'] - result['final_size_mb']
            total_savings_mb += savings_mb
            successful_compressions += 1
            print(f"✅ {result['final_size_mb']:.1f}MB ({result['savings_percent']:.1f}% smaller)")
        elif result['status'] == 'skipped':
            print(f"⏭️  {result['reason']}")
        else:
            print(f"❌ Error: {result['error']}")

    print(f"\n🎉 Compression complete!")
    print(f"   • {successful_compressions} images compressed")
    print(f"   • {total_savings_mb:.1f}MB saved")
    print(f"   • Backups created with .original extension")


if __name__ == '__main__':
    main()