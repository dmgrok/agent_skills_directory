#!/usr/bin/env python3
"""
Skill Validation Module

Performs comprehensive validation of skills before publishing:
- Schema validation
- Content quality checks
- Duplicate detection
- Security checks

Uses industry-standard libraries when available:
- detect-secrets: Secret detection (Yelp)
- semver: Semantic versioning validation
- rapidfuzz/Levenshtein: Fast string similarity

Falls back to built-in implementations when libraries are not installed.
"""

import json
import re
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional, Pattern, ClassVar

# =============================================================================
# Optional Dependencies - Graceful Degradation
# =============================================================================

# Secret detection: prefer detect-secrets library
_HAS_DETECT_SECRETS = False
try:
    from detect_secrets import SecretsCollection
    from detect_secrets.settings import transient_settings
    _HAS_DETECT_SECRETS = True
except ImportError:
    pass

# Semver validation: prefer semver library
_HAS_SEMVER = False
try:
    import semver as semver_lib
    _HAS_SEMVER = True
except ImportError:
    pass

# String similarity: prefer rapidfuzz > python-Levenshtein > built-in
_HAS_RAPIDFUZZ = False
_HAS_LEVENSHTEIN = False
try:
    from rapidfuzz.distance import Levenshtein as RapidLevenshtein
    _HAS_RAPIDFUZZ = True
except ImportError:
    try:
        import Levenshtein as LevenshteinLib
        _HAS_LEVENSHTEIN = True
    except ImportError:
        pass


def _get_available_libraries() -> Dict[str, bool]:
    """Return dict of available optional libraries."""
    return {
        'detect-secrets': _HAS_DETECT_SECRETS,
        'semver': _HAS_SEMVER,
        'rapidfuzz': _HAS_RAPIDFUZZ,
        'python-Levenshtein': _HAS_LEVENSHTEIN,
    }


# =============================================================================
# Pattern Definitions (Fallback when detect-secrets unavailable)
# =============================================================================

class Severity(Enum):
    """Severity levels for pattern matches."""
    ERROR = auto()
    WARNING = auto()
    INFO = auto()


@dataclass(frozen=True)
class SecurityPattern:
    """Immutable definition for a security-sensitive pattern."""
    name: str
    pattern: Pattern[str]
    description: str
    severity: Severity = Severity.ERROR
    
    @classmethod
    def compile(cls, name: str, regex: str, description: str, 
                severity: Severity = Severity.ERROR, flags: int = re.IGNORECASE) -> 'SecurityPattern':
        """Factory method to compile a pattern."""
        return cls(name=name, pattern=re.compile(regex, flags), description=description, severity=severity)


class SecretPatterns:
    """
    Registry of patterns for detecting accidentally committed secrets.
    
    NOTE: This is a fallback implementation. When detect-secrets is installed,
    that library's detectors are used instead (more accurate, maintained by Yelp).
    
    Patterns are based on known secret formats from various providers.
    References:
    - https://docs.github.com/en/code-security/secret-scanning/secret-scanning-patterns
    - https://docs.gitguardian.com/secrets-detection/detectors/supported_credentials
    """
    
    # OpenAI API keys: sk-<48 alphanumeric chars> or sk-proj-<48 chars>
    OPENAI_API_KEY = SecurityPattern.compile(
        "openai_api_key",
        r'\bsk-(?:proj-)?[A-Za-z0-9]{32,}(?:T3BlbkFJ[A-Za-z0-9]{20,})?\b',
        "OpenAI API key"
    )
    
    # GitHub tokens (classic PAT, fine-grained, OAuth, etc.)
    GITHUB_PAT = SecurityPattern.compile(
        "github_pat",
        r'\bghp_[A-Za-z0-9]{36,}\b',
        "GitHub Personal Access Token"
    )
    GITHUB_OAUTH = SecurityPattern.compile(
        "github_oauth",
        r'\bgho_[A-Za-z0-9]{36,}\b',
        "GitHub OAuth Token"
    )
    GITHUB_APP = SecurityPattern.compile(
        "github_app",
        r'\b(?:ghu|ghs)_[A-Za-z0-9]{36,}\b',
        "GitHub App Token"
    )
    GITHUB_REFRESH = SecurityPattern.compile(
        "github_refresh",
        r'\bghr_[A-Za-z0-9]{36,}\b',
        "GitHub Refresh Token"
    )
    GITHUB_FINE_GRAINED = SecurityPattern.compile(
        "github_fine_grained",
        r'\bgithub_pat_[A-Za-z0-9]{22}_[A-Za-z0-9]{59}\b',
        "GitHub Fine-Grained PAT"
    )
    
    # AWS credentials
    AWS_ACCESS_KEY = SecurityPattern.compile(
        "aws_access_key",
        r'\b(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}\b',
        "AWS Access Key ID",
        flags=0  # Case-sensitive
    )
    AWS_SECRET_KEY = SecurityPattern.compile(
        "aws_secret_key",
        r'(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])',
        "Possible AWS Secret Access Key",
        severity=Severity.WARNING
    )
    
    # Anthropic API keys
    ANTHROPIC_API_KEY = SecurityPattern.compile(
        "anthropic_api_key",
        r'\bsk-ant-api\d{2}-[A-Za-z0-9_-]{93}(?:AA)?\b',
        "Anthropic API key"
    )
    
    # Google Cloud / Firebase
    GOOGLE_API_KEY = SecurityPattern.compile(
        "google_api_key",
        r'\bAIza[A-Za-z0-9_-]{35}\b',
        "Google API key"
    )
    GOOGLE_OAUTH_TOKEN = SecurityPattern.compile(
        "google_oauth",
        r'\bya29\.[A-Za-z0-9_-]{50,}\b',
        "Google OAuth Access Token"
    )
    
    # Slack tokens
    SLACK_BOT_TOKEN = SecurityPattern.compile(
        "slack_bot",
        r'\bxoxb-[0-9]{10,13}-[0-9]{10,13}-[A-Za-z0-9]{24}\b',
        "Slack Bot Token"
    )
    SLACK_USER_TOKEN = SecurityPattern.compile(
        "slack_user",
        r'\bxoxp-[0-9]{10,13}-[0-9]{10,13}-[A-Za-z0-9]{24,32}\b',
        "Slack User Token"
    )
    SLACK_WEBHOOK = SecurityPattern.compile(
        "slack_webhook",
        r'\bhttps://hooks\.slack\.com/services/T[A-Z0-9]{8,}/B[A-Z0-9]{8,}/[A-Za-z0-9]{24}\b',
        "Slack Webhook URL"
    )
    
    # Stripe keys
    STRIPE_LIVE_KEY = SecurityPattern.compile(
        "stripe_live",
        r'\b(?:sk|pk)_live_[A-Za-z0-9]{24,}\b',
        "Stripe Live API key"
    )
    STRIPE_TEST_KEY = SecurityPattern.compile(
        "stripe_test",
        r'\b(?:sk|pk)_test_[A-Za-z0-9]{24,}\b',
        "Stripe Test API key",
        severity=Severity.WARNING
    )
    
    # Discord tokens
    DISCORD_TOKEN = SecurityPattern.compile(
        "discord_token",
        r'\b[MN][A-Za-z\d]{23,}\.[\w-]{6}\.[\w-]{27,}\b',
        "Discord Bot Token"
    )
    DISCORD_WEBHOOK = SecurityPattern.compile(
        "discord_webhook",
        r'\bhttps://(?:ptb\.|canary\.)?discord(?:app)?\.com/api/webhooks/\d+/[A-Za-z0-9_-]+\b',
        "Discord Webhook URL"
    )
    
    # npm tokens
    NPM_TOKEN = SecurityPattern.compile(
        "npm_token",
        r'\bnpm_[A-Za-z0-9]{36}\b',
        "npm Access Token"
    )
    
    # PyPI tokens
    PYPI_TOKEN = SecurityPattern.compile(
        "pypi_token",
        r'\bpypi-AgE[A-Za-z0-9_-]{50,}\b',
        "PyPI API Token"
    )
    
    # Twilio
    TWILIO_API_KEY = SecurityPattern.compile(
        "twilio_api",
        r'\bSK[a-f0-9]{32}\b',
        "Twilio API Key"
    )
    
    # SendGrid
    SENDGRID_API_KEY = SecurityPattern.compile(
        "sendgrid_api",
        r'\bSG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}\b',
        "SendGrid API Key"
    )
    
    # Generic patterns (lower confidence)
    GENERIC_API_KEY = SecurityPattern.compile(
        "generic_api_key",
        r'(?:api[_-]?key|apikey)\s*[:=]\s*["\']?([A-Za-z0-9_-]{20,})["\']?',
        "Generic API key assignment",
        severity=Severity.WARNING
    )
    GENERIC_SECRET = SecurityPattern.compile(
        "generic_secret",
        r'(?:secret|password|passwd|pwd)\s*[:=]\s*["\']?([^\s"\']{8,})["\']?',
        "Generic secret assignment",
        severity=Severity.WARNING
    )
    GENERIC_TOKEN = SecurityPattern.compile(
        "generic_token",
        r'(?:token|auth[_-]?token|access[_-]?token)\s*[:=]\s*["\']?([A-Za-z0-9_-]{20,})["\']?',
        "Generic token assignment",
        severity=Severity.WARNING
    )
    
    # Private keys
    PRIVATE_KEY_HEADER = SecurityPattern.compile(
        "private_key",
        r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----',
        "Private key detected"
    )
    
    @classmethod
    def all_patterns(cls) -> List[SecurityPattern]:
        """Return all registered security patterns."""
        return [
            getattr(cls, attr) for attr in dir(cls)
            if isinstance(getattr(cls, attr), SecurityPattern)
        ]


class MaliciousPatterns:
    """
    Registry of patterns for detecting potentially malicious code.
    """
    
    # Dangerous shell commands
    DESTRUCTIVE_RM = SecurityPattern.compile(
        "destructive_rm",
        r'\brm\s+(?:-[rfv]+\s+)*(?:/|~|\$HOME|\$\{HOME\}|/etc|/usr|/var)',
        "Destructive rm command targeting system directories",
        severity=Severity.ERROR
    )
    
    # Remote code execution patterns
    CURL_PIPE_BASH = SecurityPattern.compile(
        "curl_pipe_bash",
        r'\bcurl\s+[^\|]*\|\s*(?:ba)?sh\b',
        "Piping curl output directly to shell"
    )
    WGET_PIPE_SH = SecurityPattern.compile(
        "wget_pipe_sh",
        r'\bwget\s+[^\|]*\|\s*(?:ba)?sh\b',
        "Piping wget output directly to shell"
    )
    CURL_PIPE_PYTHON = SecurityPattern.compile(
        "curl_pipe_python",
        r'\bcurl\s+[^\|]*\|\s*python[3]?\b',
        "Piping curl output to Python interpreter",
        severity=Severity.WARNING
    )
    
    # Code injection vectors
    PYTHON_EVAL = SecurityPattern.compile(
        "python_eval",
        r'\beval\s*\([^)]*(?:input|request|argv|environ)',
        "eval() with untrusted input",
        severity=Severity.WARNING
    )
    PYTHON_EXEC = SecurityPattern.compile(
        "python_exec",
        r'\bexec\s*\([^)]*(?:input|request|argv|environ)',
        "exec() with untrusted input",
        severity=Severity.WARNING
    )
    PYTHON_DYNAMIC_IMPORT = SecurityPattern.compile(
        "python_dynamic_import",
        r'\b__import__\s*\([^)]*(?:input|request|argv)',
        "__import__() with untrusted input",
        severity=Severity.WARNING
    )
    
    # Subprocess with shell=True
    SUBPROCESS_SHELL = SecurityPattern.compile(
        "subprocess_shell",
        r'\bsubprocess\.(?:call|run|Popen)\s*\([^)]*shell\s*=\s*True',
        "subprocess with shell=True",
        severity=Severity.WARNING
    )
    
    # SQL injection indicators
    SQL_STRING_CONCAT = SecurityPattern.compile(
        "sql_injection",
        r'(?:SELECT|INSERT|UPDATE|DELETE|DROP)\s+[^;]*\+\s*(?:request|input|argv)',
        "Possible SQL injection via string concatenation",
        severity=Severity.WARNING
    )
    
    # Obfuscation indicators
    BASE64_DECODE_EXEC = SecurityPattern.compile(
        "base64_exec",
        r'\bbase64\.b64decode\s*\([^)]+\).*(?:eval|exec)',
        "Base64 decode followed by code execution",
        severity=Severity.WARNING
    )
    
    @classmethod
    def all_patterns(cls) -> List[SecurityPattern]:
        """Return all registered malicious patterns."""
        return [
            getattr(cls, attr) for attr in dir(cls)
            if isinstance(getattr(cls, attr), SecurityPattern)
        ]


class ContentQualityPatterns:
    """Patterns for detecting content quality issues."""
    
    # Placeholder text patterns (compiled once)
    PLACEHOLDER_TODO = re.compile(r'\bTODO\b', re.IGNORECASE)
    PLACEHOLDER_FIXME = re.compile(r'\bFIXME\b', re.IGNORECASE)
    PLACEHOLDER_TBD = re.compile(r'\bTBD\b', re.IGNORECASE)
    PLACEHOLDER_LOREM = re.compile(r'\bLorem\s+ipsum\b', re.IGNORECASE)
    PLACEHOLDER_GENERIC = re.compile(
        r'\b(?:placeholder|add\s+your\s+content|example\s+here|describe\s+how)\b',
        re.IGNORECASE
    )
    
    # Markdown section headers
    USAGE_SECTION = re.compile(r'^#+\s*(?:usage|how\s+to\s+use|getting\s+started)\s*$', re.IGNORECASE | re.MULTILINE)
    EXAMPLE_SECTION = re.compile(r'^#+\s*(?:examples?|samples?)\s*$', re.IGNORECASE | re.MULTILINE)
    
    # Code block detection
    FENCED_CODE_BLOCK = re.compile(r'```[\s\S]*?```')
    INDENTED_CODE_BLOCK = re.compile(r'^(?:    |\t)[^\s]', re.MULTILINE)
    
    PLACEHOLDERS: ClassVar[List[Tuple[Pattern[str], str]]] = []
    
    @classmethod
    def get_placeholder_patterns(cls) -> List[Tuple[Pattern[str], str]]:
        """Return list of (pattern, description) for placeholder detection."""
        return [
            (cls.PLACEHOLDER_TODO, "TODO"),
            (cls.PLACEHOLDER_FIXME, "FIXME"),
            (cls.PLACEHOLDER_TBD, "TBD"),
            (cls.PLACEHOLDER_LOREM, "Lorem ipsum"),
            (cls.PLACEHOLDER_GENERIC, "placeholder text"),
        ]


class NameValidationPatterns:
    """Patterns for validating names and identifiers."""
    
    # Valid skill name: lowercase alphanumeric with hyphens, not starting/ending with hyphen
    VALID_SKILL_NAME = re.compile(r'^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$')
    
    # Semver: MAJOR.MINOR.PATCH[-prerelease][+build]
    SEMVER = re.compile(
        r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)'
        r'(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
        r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?'
        r'(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
    )
    
    # Reserved/generic names to warn about
    RESERVED_NAMES: ClassVar[frozenset] = frozenset([
        'test', 'example', 'skill', 'agent', 'cli', 'api', 'core', 'base',
        'null', 'undefined', 'none', 'default', 'main', 'index', 'app',
        'demo', 'sample', 'template', 'starter', 'boilerplate'
    ])


# =============================================================================
# Validation Classes
# =============================================================================

class ValidationResult:
    """Result of a validation check."""
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
    
    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0
    
    def add_error(self, msg: str):
        self.errors.append(msg)
    
    def add_warning(self, msg: str):
        self.warnings.append(msg)
    
    def add_info(self, msg: str):
        self.info.append(msg)
    
    def merge(self, other: 'ValidationResult'):
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.info.extend(other.info)


def validate_skill_name(name: str) -> ValidationResult:
    """Validate skill name format."""
    result = ValidationResult()
    
    if not name:
        result.add_error("Skill name is required")
        return result
    
    # Must be lowercase
    if name != name.lower():
        result.add_error(f"Skill name must be lowercase: '{name}'")
    
    # Validate format using compiled pattern
    if not NameValidationPatterns.VALID_SKILL_NAME.match(name):
        result.add_error(
            f"Invalid skill name '{name}'. Must be lowercase alphanumeric with hyphens, "
            "cannot start or end with a hyphen."
        )
    
    # Length limits
    if len(name) < 2:
        result.add_error("Skill name must be at least 2 characters")
    elif len(name) > 50:
        result.add_error("Skill name must be 50 characters or less")
    
    # Reserved/generic names
    if name.lower() in NameValidationPatterns.RESERVED_NAMES:
        result.add_warning(f"'{name}' is a reserved/generic name. Consider a more descriptive name.")
    
    return result


def validate_version(version: str) -> ValidationResult:
    """
    Validate semantic version format (semver 2.0.0 compliant).
    
    Uses the `semver` library when available for full spec compliance,
    falls back to regex-based validation otherwise.
    """
    result = ValidationResult()
    
    if not version:
        result.add_error("Version is required")
        return result
    
    # Use semver library if available (full spec compliance)
    if _HAS_SEMVER:
        try:
            parsed = semver_lib.Version.parse(version)
            # Warn about 0.x versions (pre-release/unstable)
            if parsed.major == 0:
                result.add_info("Version 0.x indicates pre-release/unstable")
            return result
        except ValueError as e:
            result.add_error(
                f"Invalid version '{version}'. Use semver format "
                f"(e.g., 1.0.0, 1.0.0-beta.1, 1.0.0-rc.1+build.123)"
            )
            return result
    
    # Fallback: Validate against regex pattern
    match = NameValidationPatterns.SEMVER.match(version)
    if not match:
        result.add_error(
            f"Invalid version '{version}'. Use semver format "
            "(e.g., 1.0.0, 1.0.0-beta.1, 1.0.0-rc.1+build.123)"
        )
        return result
    
    # Warn about 0.x versions (pre-release/unstable)
    if match.group('major') == '0':
        result.add_info("Version 0.x indicates pre-release/unstable")
    
    return result


def validate_skill_json(manifest: Dict[str, Any]) -> ValidationResult:
    """Validate skill.json manifest."""
    result = ValidationResult()
    
    # Required fields
    required = ['name', 'version', 'description']
    for field in required:
        if not manifest.get(field):
            result.add_error(f"Missing required field: {field}")
    
    # Validate name
    if manifest.get('name'):
        result.merge(validate_skill_name(manifest['name']))
    
    # Validate version
    if manifest.get('version'):
        result.merge(validate_version(manifest['version']))
    
    # Description quality
    desc = manifest.get('description', '')
    if desc and len(desc) < 10:
        result.add_warning("Description is very short. Consider adding more detail.")
    if desc and len(desc) > 200:
        result.add_warning("Description is long. Consider shortening to ~150 characters.")
    
    # Keywords validation
    keywords = manifest.get('keywords', [])
    if not keywords:
        result.add_warning("No keywords specified. Keywords help with discoverability.")
    elif len(keywords) > 10:
        result.add_warning("Too many keywords (max 10 recommended)")
    
    # Runtime validation
    valid_runtimes = ['universal', 'mcp', 'langchain', 'crewai', 'autogen', 'openai', 'anthropic']
    runtime = manifest.get('runtime', 'universal')
    if runtime not in valid_runtimes:
        result.add_warning(f"Unknown runtime '{runtime}'. Known runtimes: {', '.join(valid_runtimes)}")
    
    # Capabilities validation
    valid_capabilities = [
        'web-browsing', 'file-system', 'code-execution', 'api-access',
        'database', 'shell-access', 'network', 'multimedia', 'delegation'
    ]
    for cap in manifest.get('capabilities', []):
        if cap not in valid_capabilities:
            result.add_info(f"Custom capability: {cap}")
    
    # License check
    if not manifest.get('license'):
        result.add_warning("No license specified. Consider adding a license (MIT, Apache-2.0, etc.)")
    
    return result


def validate_skill_md(content: str) -> ValidationResult:
    """Validate SKILL.md content quality."""
    result = ValidationResult()
    
    if not content or not content.strip():
        result.add_error("SKILL.md is empty")
        return result
    
    # Minimum length
    if len(content.strip()) < 100:
        result.add_error("SKILL.md is too short (minimum 100 characters). Add meaningful instructions.")
    
    # Check for placeholder content using compiled patterns
    for pattern, description in ContentQualityPatterns.get_placeholder_patterns():
        if pattern.search(content):
            result.add_warning(f"Contains placeholder text: '{description}'")
    
    # Check for common sections using compiled patterns
    if not ContentQualityPatterns.USAGE_SECTION.search(content):
        result.add_info("Consider adding a 'Usage' section")
    if not ContentQualityPatterns.EXAMPLE_SECTION.search(content):
        result.add_info("Consider adding an 'Examples' section")
    
    # Check for code blocks using compiled patterns
    has_fenced = ContentQualityPatterns.FENCED_CODE_BLOCK.search(content) is not None
    has_indented = ContentQualityPatterns.INDENTED_CODE_BLOCK.search(content) is not None
    if not has_fenced and not has_indented:
        result.add_info("Consider adding code examples in fenced code blocks")
    
    # Word count check
    words = len(content.split())
    if words < 50:
        result.add_warning(f"SKILL.md has only {words} words. More detailed instructions recommended.")
    elif words > 5000:
        result.add_info(f"SKILL.md is quite long ({words} words). Consider splitting into sections.")
    
    return result


def _scan_secrets_with_detect_secrets(content: str) -> List[Tuple[str, str]]:
    """
    Use detect-secrets library to scan content for secrets.
    
    Returns list of (secret_type, description) tuples.
    """
    import tempfile
    import os
    
    findings = []
    
    # detect-secrets works with files, so we need to write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(content)
        temp_path = f.name
    
    try:
        secrets = SecretsCollection()
        # Configure all available plugins for comprehensive detection
        # See: detect-secrets scan --list-all-plugins
        with transient_settings({
            'plugins_used': [
                # Cloud provider keys
                {'name': 'AWSKeyDetector'},
                {'name': 'AzureStorageKeyDetector'},
                {'name': 'IbmCloudIamDetector'},
                {'name': 'IbmCosHmacDetector'},
                {'name': 'SoftlayerDetector'},
                # Code hosting & CI/CD
                {'name': 'GitHubTokenDetector'},
                {'name': 'GitLabTokenDetector'},
                {'name': 'NpmDetector'},
                {'name': 'PypiTokenDetector'},
                {'name': 'ArtifactoryDetector'},
                # AI/ML API keys  
                {'name': 'OpenAIDetector'},
                # Communication platforms
                {'name': 'SlackDetector'},
                {'name': 'DiscordBotTokenDetector'},
                {'name': 'TelegramBotTokenDetector'},
                {'name': 'MailchimpDetector'},
                {'name': 'TwilioKeyDetector'},
                {'name': 'SendGridDetector'},
                # Payment & SaaS
                {'name': 'StripeDetector'},
                {'name': 'SquareOAuthDetector'},
                {'name': 'CloudantDetector'},
                # Auth & generic
                {'name': 'BasicAuthDetector'},
                {'name': 'JwtTokenDetector'},
                {'name': 'PrivateKeyDetector'},
                {'name': 'KeywordDetector'},
                # Entropy-based detection (catches unknown formats)
                {'name': 'Base64HighEntropyString', 'limit': 4.5},
                {'name': 'HexHighEntropyString', 'limit': 3.0},
            ],
        }):
            secrets.scan_file(temp_path)
        
        # Extract findings
        for filename, secret_list in secrets.data.items():
            for secret in secret_list:
                findings.append((secret.type, f"{secret.type} detected"))
    finally:
        os.unlink(temp_path)
    
    return findings


def validate_no_secrets(content: str) -> ValidationResult:
    """
    Check for accidentally committed secrets.
    
    Uses detect-secrets library (Yelp) when available for industry-standard
    detection with 20+ detectors including entropy analysis.
    Falls back to built-in regex patterns otherwise.
    """
    result = ValidationResult()
    
    # Use detect-secrets library if available (preferred)
    if _HAS_DETECT_SECRETS:
        try:
            findings = _scan_secrets_with_detect_secrets(content)
            for secret_type, description in findings:
                result.add_error(f"Security: {description}")
            return result
        except Exception:
            # Fall through to regex-based detection on error
            pass
    
    # Fallback: Use built-in regex patterns
    for pattern in SecretPatterns.all_patterns():
        match = pattern.pattern.search(content)
        if match:
            message = f"Security: {pattern.description} detected"
            if pattern.severity == Severity.ERROR:
                result.add_error(message)
            elif pattern.severity == Severity.WARNING:
                result.add_warning(message)
            else:
                result.add_info(message)
    
    return result


def validate_no_malicious_patterns(content: str) -> ValidationResult:
    """
    Check for potentially malicious patterns.
    
    Detects dangerous commands, code injection vectors, and obfuscation techniques.
    """
    result = ValidationResult()
    
    for pattern in MaliciousPatterns.all_patterns():
        match = pattern.pattern.search(content)
        if match:
            message = f"Security review needed: {pattern.description}"
            if pattern.severity == Severity.ERROR:
                result.add_error(message)
            elif pattern.severity == Severity.WARNING:
                result.add_warning(message)
            else:
                result.add_info(message)
    
    return result


def _levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate the Levenshtein distance between two strings.
    
    Uses rapidfuzz or python-Levenshtein when available (C-optimized),
    falls back to pure Python dynamic programming implementation.
    """
    # Use rapidfuzz if available (fastest)
    if _HAS_RAPIDFUZZ:
        return RapidLevenshtein.distance(s1, s2)
    
    # Use python-Levenshtein if available
    if _HAS_LEVENSHTEIN:
        return LevenshteinLib.distance(s1, s2)
    
    # Fallback: Pure Python implementation with O(min(m,n)) space
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost is 0 if characters match, 1 otherwise
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def _similarity_ratio(s1: str, s2: str) -> float:
    """
    Calculate similarity ratio between two strings (0.0 to 1.0).
    
    Uses rapidfuzz's normalized_similarity when available (faster, more features),
    falls back to Levenshtein-based calculation.
    
    Returns 1.0 for identical strings, 0.0 for completely different strings.
    """
    if not s1 or not s2:
        return 0.0
    if s1 == s2:
        return 1.0
    
    # Use rapidfuzz's normalized similarity if available
    if _HAS_RAPIDFUZZ:
        return RapidLevenshtein.normalized_similarity(s1, s2)
    
    # Use python-Levenshtein ratio if available
    if _HAS_LEVENSHTEIN:
        return LevenshteinLib.ratio(s1, s2)
    
    # Fallback: Calculate from distance
    distance = _levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    return 1.0 - (distance / max_len)


def check_duplicate_name(skill_name: str, catalog: Dict[str, Any]) -> ValidationResult:
    """
    Check if skill name already exists or is too similar to existing names.
    
    Uses Levenshtein distance for proper similarity detection.
    """
    result = ValidationResult()
    
    skill_lower = skill_name.lower()
    similar_names: List[Tuple[str, float]] = []
    
    for skill in catalog.get('skills', []):
        existing_name = skill.get('name', '').lower()
        existing_id = skill.get('id', '')
        
        if not existing_name:
            continue
        
        # Check exact name match
        if skill_lower == existing_name:
            result.add_error(f"Skill name '{skill_name}' already exists: {existing_id}")
            continue
        
        # Calculate similarity ratio
        ratio = _similarity_ratio(skill_lower, existing_name)
        
        # High similarity threshold (>0.8 means very similar)
        if ratio > 0.8:
            similar_names.append((existing_name, ratio))
    
    # Report similar names (sorted by similarity)
    if similar_names:
        similar_names.sort(key=lambda x: x[1], reverse=True)
        for name, ratio in similar_names[:3]:  # Report top 3 similar names
            result.add_warning(
                f"Similar skill name exists: '{name}' ({ratio:.0%} similar)"
            )
    
    return result


def validate_skill_directory(skill_dir: Path, catalog: Optional[Dict[str, Any]] = None) -> ValidationResult:
    """
    Comprehensive validation of a skill directory.
    
    Args:
        skill_dir: Path to skill directory
        catalog: Optional catalog for duplicate checking
    
    Returns:
        ValidationResult with all errors, warnings, and info
    """
    result = ValidationResult()
    
    skill_dir = Path(skill_dir)
    
    if not skill_dir.exists():
        result.add_error(f"Directory not found: {skill_dir}")
        return result
    
    if not skill_dir.is_dir():
        result.add_error(f"Not a directory: {skill_dir}")
        return result
    
    # Validate skill.json
    manifest_path = skill_dir / "skill.json"
    manifest = {}
    
    if not manifest_path.exists():
        result.add_error("skill.json not found. Run 'skills init' first.")
    else:
        try:
            manifest = json.loads(manifest_path.read_text())
            result.merge(validate_skill_json(manifest))
            
            # Security check on manifest
            result.merge(validate_no_secrets(json.dumps(manifest)))
        except json.JSONDecodeError as e:
            result.add_error(f"Invalid JSON in skill.json: {e}")
    
    # Validate SKILL.md
    skill_md_path = skill_dir / "SKILL.md"
    
    if not skill_md_path.exists():
        result.add_error("SKILL.md not found. Create a SKILL.md with your skill instructions.")
    else:
        content = skill_md_path.read_text()
        result.merge(validate_skill_md(content))
        result.merge(validate_no_secrets(content))
        result.merge(validate_no_malicious_patterns(content))
    
    # Check for duplicate names in catalog
    if catalog and manifest.get('name'):
        result.merge(check_duplicate_name(manifest['name'], catalog))
    
    # Check for recommended files
    if not (skill_dir / "LICENSE").exists() and not (skill_dir / "LICENSE.md").exists():
        result.add_info("Consider adding a LICENSE file")
    
    if not (skill_dir / "README.md").exists():
        result.add_info("Consider adding a README.md for GitHub display")
    
    return result


def format_validation_result(result: ValidationResult, verbose: bool = True) -> str:
    """Format validation result for display."""
    lines = []
    
    if result.errors:
        lines.append("\n❌ Errors (must fix):")
        for err in result.errors:
            lines.append(f"   • {err}")
    
    if result.warnings:
        lines.append("\n⚠️  Warnings (should fix):")
        for warn in result.warnings:
            lines.append(f"   • {warn}")
    
    if verbose and result.info:
        lines.append("\nℹ️  Suggestions:")
        for info in result.info:
            lines.append(f"   • {info}")
    
    if result.is_valid:
        if not result.warnings:
            lines.append("\n✅ Validation passed!")
        else:
            lines.append("\n✅ Validation passed with warnings")
    else:
        lines.append(f"\n❌ Validation failed ({len(result.errors)} error(s))")
    
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        skill_dir = Path(sys.argv[1])
        result = validate_skill_directory(skill_dir)
        print(format_validation_result(result))
        sys.exit(0 if result.is_valid else 1)
    else:
        print("Usage: python validate.py <skill-directory>")
        sys.exit(1)
