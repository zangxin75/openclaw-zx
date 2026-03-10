---
name: imap-smtp-email
description: |
  Read and send email via IMAP/SMTP. Check for new/unread messages, fetch content, search mailboxes, mark as read/unread, and send emails with attachments. Works with any IMAP/SMTP server including Gmail, Outlook, 163.com, vip.163.com, 126.com, and vip.126.com.
---

# IMAP/SMTP Email Tool

Read and send email via IMAP/SMTP protocol.

## Quick Setup

1. **Create `.env` file** in skill directory with credentials:

```bash
# IMAP Configuration (receiving email)
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USER=your@gmail.com
IMAP_PASS=your_app_password
IMAP_TLS=true
IMAP_MAILBOX=INBOX

# SMTP Configuration (sending email)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your@gmail.com
SMTP_PASS=your_app_password
SMTP_FROM=your@gmail.com
```

2. **Install dependencies:**
```bash
cd ~/.openclaw/workspace/skills/imap-smtp-email && npm install
```

## IMAP Commands (Receiving Email)

### Check for new emails
```bash
node scripts/imap.js check --limit 10
node scripts/imap.js check --recent 2h        # Last 2 hours
node scripts/imap.js check --recent 30m       # Last 30 minutes
```

### Fetch specific email
```bash
node scripts/imap.js fetch <uid>
```

### Search emails
```bash
node scripts/imap.js search --unseen
node scripts/imap.js search --from "sender@example.com"
node scripts/imap.js search --subject "important"
```

### Mark as read/unread
```bash
node scripts/imap.js mark-read <uid>
node scripts/imap.js mark-unread <uid>
```

## SMTP Commands (Sending Email)

### Send email
```bash
# Simple text email
node scripts/smtp.js send --to recipient@example.com --subject "Hello" --body "World"

# HTML email
node scripts/smtp.js send --to recipient@example.com --subject "Newsletter" --html --body "<h1>Welcome</h1>"

# Email with attachment
node scripts/smtp.js send --to recipient@example.com --subject "Report" --body "Please find attached" --attach report.pdf
```

## Common Email Servers

| Provider | IMAP Host | IMAP Port | SMTP Host | SMTP Port |
|----------|-----------|-----------|-----------|-----------|
| 163.com | imap.163.com | 993 | smtp.163.com | 465 |
| vip.163.com | imap.vip.163.com | 993 | smtp.vip.163.com | 465 |
| 126.com | imap.126.com | 993 | smtp.126.com | 465 |
| Gmail | imap.gmail.com | 993 | smtp.gmail.com | 587 |
| Outlook | outlook.office365.com | 993 | smtp.office365.com | 587 |
| QQ Mail | imap.qq.com | 993 | smtp.qq.com | 587 |

**Important for 163.com:** Use **authorization code** (授权码), not account password
