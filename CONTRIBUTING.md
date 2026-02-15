# Contributing to CineMatch

First off, thank you for considering contributing to CineMatch! 🎬

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide detailed description** of the proposed feature
- **Explain why this enhancement would be useful**
- **Include mockups** if relevant

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code, add tests
3. Ensure the test suite passes
4. Make sure your code follows the existing style
5. Write a clear commit message

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/cinematch.git
cd cinematch

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_streamlit.txt

# Run tests
python test_api.py
```

## Styleguides

### Git Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and PRs liberally

Examples:
```
feat: Add genre filter to recommendations
fix: Resolve session timeout issue
docs: Update deployment guide
style: Format code with black
test: Add tests for user validation
```

### Python Styleguide

- Follow [PEP 8](https://pep8.org/)
- Use type hints where applicable
- Write docstrings for functions
- Keep functions focused and small
- Use meaningful variable names

### Documentation Styleguide

- Use Markdown for documentation
- Include code examples where relevant
- Keep language clear and concise
- Update README if you add new features

## Code Review Process

- Maintainers will review PRs within 7 days
- Address review comments promptly
- Be open to feedback and discussion
- Once approved, your PR will be merged

## Community

- Be respectful and constructive
- Welcome newcomers and encourage questions
- Give credit where credit is due
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)

## Questions?

Feel free to open an issue with your question or contact the maintainers directly.

Thank you for contributing! 🙏
