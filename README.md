# Project Documentation

## Overview
This project provides an automated solution for uploading videos to various social media platforms, including Instagram, TikTok, and YouTube. The application allows users to configure multiple accounts and schedule video uploads, streamlining the content-sharing process.

## Installation and Setup

### Windows
1. Run the following commands in the command prompt to set up the environment on Windows.

### Unix-Based Systems
1. Run the following commands in the terminal to set up the environment on Unix-based systems.

## Configuration

1. Execute `add_account.py` to set up your social media accounts. This script will guide you through logging into Instagram, TikTok, and YouTube and store your session information.
2. The script will prompt you to choose a default folder for your videos and to enter a default caption.

## Running the Application

### Scheduling Tasks in Windows
1. Modify `sample.bat` with the correct paths to your virtual environment and `main.py`, and replace `account_name` with the actual account name.

### Manual Execution
1. Run `main.py` directly to upload a video immediately.
   - The script selects a random video from your designated folder, uploads it to the configured accounts, and moves the video to a 'used' folder.

## Note
- The scheduler for Unix systems is currently under development and not available.
- The application relies on the Playwright library to automate web interactions for account logins and uploads.

## Conclusion
This Markdown documentation provides a clear guide for users to set up and use the project. The application simplifies the process of managing video uploads across multiple social media platforms, offering an automated and user-friendly approach.
