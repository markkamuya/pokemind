# Security

## Reporting

Open a private security advisory for vulnerabilities in the public utilities.

## Credential hygiene

This project never needs committed credentials. Keep Kaggle and other service
tokens in the provider's credential store or in ignored environment files.

Before publishing a branch:

1. Review `git status`.
2. Search for token prefixes, bearer headers, passwords, and private keys.
3. Inspect every file larger than 1 MB.
4. Confirm that no simulator binary, replay archive, or submission package is
   staged.

If a credential is ever pasted into a chat, terminal log, commit, or issue,
revoke it and generate a replacement.
