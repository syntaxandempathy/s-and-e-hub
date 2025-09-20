# Image Compression Tools

*A collection of Python scripts for optimizing images.*

**Overview**

This directory contains Python scripts designed to compress images, primarily PNG and JPEG files.  These tools are useful for reducing the size of image assets within projects, particularly large image sets associated with articles or documentation. The scripts are designed for batch processing, allowing for efficient compression of multiple images at once.  They offer options for adjusting compression quality and size thresholds.  These tools are specifically designed for the Syntax & Empathy project.

**Contents**

* `compress_images.py`: A Python script to compress PNG and JPEG images using adjustable quality and size parameters.

**Usage**

To compress images in the `../articles` directory, maintaining at least 85% quality and a maximum size of 2MB, use the following command:

```bash
python compress_images.py --directory ../articles --quality 85 --size-threshold 2
```

**Conventions**

All scripts are written in Python 3 and utilize the `argparse` module for command-line argument parsing.  The scripts are designed to be easily adaptable to different project needs through configuration options.


Last updated: 2025-09-20
