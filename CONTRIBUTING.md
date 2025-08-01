# 🤝 Contributing to QASports

We warmly welcome contributions from the community! Whether you're a researcher, developer, or sports enthusiast, your contributions help make QASports better for everyone.

## 🌟 How You Can Contribute

### 🐛 Report Issues
- Found a bug? Report it on [GitHub Issues](https://github.com/leomaurodesenv/qasports-dataset-scripts/issues)
- Include detailed steps to reproduce the problem
- Share your environment details (Python version, OS, etc.)

### 💡 Suggest Improvements
- Have ideas for new features? We'd love to hear them!
- Propose enhancements to the dataset generation pipeline
- Suggest new sports or data sources to include
- Recommend improvements to documentation or experiments

### 🔧 Fix Issues
- Browse our [open issues](https://github.com/leomaurodesenv/qasports-dataset-scripts/issues)
- Pick an issue that interests you
- Comment on the issue to let us know you're working on it
- Submit a pull request with your fix

### 📚 Improve Documentation
- Help improve our README, code comments, or docstrings
- Add examples or tutorials
- Translate documentation to other languages
- Create guides for specific use cases

### 🧪 Enhance Experiments
- Improve existing experiment frameworks
- Add new evaluation metrics
- Implement new models or approaches
- Create benchmark comparisons

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- [uv](https://github.com/astral-sh/uv) package manager
- Git

### Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/qasports-dataset-scripts.git
cd qasports-dataset-scripts

# Add the original repository as upstream
git remote add upstream https://github.com/leomaurodesenv/qasports-dataset-scripts.git

# Install dependencies
uv sync

# Install development dependencies
uv sync --group dev

# Set up pre-commit hooks
uv run pre-commit install
```

### Development Workflow

```bash
# Create a new branch for your work
git checkout -b feature/your-feature-name

# Make your changes
# ... edit files ...

# Run tests and checks
uv run pre-commit run --all-files

# Commit your changes
git add .
git commit -m "feat: add your feature description"

# Push to your fork
git push origin feature/your-feature-name
```

## 📋 Contribution Guidelines

### Code Style
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use [ruff](https://github.com/astral-sh/ruff) for linting and formatting
- Write clear, descriptive commit messages
- Add type hints where appropriate

### Commit Message Format
We use [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat: add new sports data source`
- `fix(experiments): resolve pkg_resources import error`
- `docs: improve README installation instructions`
- `test: add unit tests for data processing`

### Pull Request Process

1. **Fork the repository** and create a feature branch
2. **Make your changes** following the code style guidelines
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Submit a pull request** with a clear description

### Pull Request Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing
- [ ] I have tested my changes locally
- [ ] I have added/updated tests
- [ ] All tests pass

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have updated documentation as needed
- [ ] My changes generate no new warnings
- [ ] I have added comments to my code where necessary
```

## 🎯 Areas for Contribution

### High Priority
- **Bug fixes** in the dataset generation pipeline
- **Performance improvements** for large-scale processing
- **Documentation enhancements** and tutorials
- **Test coverage** improvements

### Medium Priority
- **New sports data sources** (tennis, baseball, hockey, etc.)
- **Enhanced experiment frameworks** with new models
- **Data quality improvements** and validation
- **Multi-language support** for questions and answers

### Low Priority
- **UI/UX improvements** for experiment interfaces
- **Additional export formats** for the dataset
- **Integration examples** with popular ML frameworks
- **Community tutorials** and use cases

## 🏷️ Issue Labels

We use labels to categorize issues:

- `good first issue` - Perfect for newcomers
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements to docs
- `help wanted` - Extra attention needed
- `question` - Further information is requested

## 🤝 Community Guidelines

### Be Respectful
- Treat all contributors with respect and kindness
- Be patient with newcomers
- Provide constructive feedback
- Celebrate others' contributions

### Be Helpful
- Answer questions when you can
- Share your knowledge and experience
- Help review pull requests
- Welcome new contributors

### Be Professional
- Keep discussions focused and on-topic
- Use clear, professional language
- Follow the project's code of conduct
- Respect maintainers' decisions

## 📞 Getting Help

### Questions?
- Check our [documentation](README.md)
- Search [existing issues](https://github.com/leomaurodesenv/qasports-dataset-scripts/issues)
- Ask in [GitHub Discussions](https://github.com/leomaurodesenv/qasports-dataset-scripts/discussions)

### Stuck?
- Don't hesitate to ask for help!
- We're here to support you
- No question is too small

## 🎉 Recognition

Contributors will be:
- Mentioned in release notes
- Acknowledged in research papers when appropriate
- Featured in our community highlights

## 📄 License

By contributing to QASports, you agree that your contributions will be licensed under the same [MIT License](LICENSE) that covers the project.

---

**Thank you for contributing to QASports!** 🏆

Your contributions help advance sports analytics and question answering research. Together, we're building the future of sports data science.
