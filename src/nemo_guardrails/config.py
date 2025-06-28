"""
Configuration management for Nvidia NeMo Guardrails.
"""

import json
import yaml
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from .models import Rule


class ConfigManager:
    """Manages guardrails configuration and rules."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.rules: List[Rule] = []
        self._loaded = False
        
    async def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Returns:
            Configuration dictionary
        """
        if self._loaded:
            return self.config
            
        if not self.config_path:
            self.config = self._get_default_config()
        else:
            config_file = Path(self.config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
                
            if config_file.suffix.lower() in ['.yaml', '.yml']:
                with open(config_file, 'r') as f:
                    self.config = yaml.safe_load(f)
            elif config_file.suffix.lower() == '.json':
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                raise ValueError(f"Unsupported configuration file format: {config_file.suffix}")
        
        # Load rules from configuration
        self.rules = self._load_rules_from_config()
        self._loaded = True
        
        return self.config
    
    async def save_config(self, config_path: Optional[str] = None) -> None:
        """
        Save configuration to file.
        
        Args:
            config_path: Path to save configuration (uses instance path if not provided)
        """
        if not self._loaded:
            await self.load_config()
            
        save_path = config_path or self.config_path
        if not save_path:
            raise ValueError("No configuration path specified")
            
        config_file = Path(save_path)
        
        # Update rules in configuration
        self.config['rules'] = [self._rule_to_dict(rule) for rule in self.rules]
        
        if config_file.suffix.lower() in ['.yaml', '.yml']:
            with open(config_file, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
        elif config_file.suffix.lower() == '.json':
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        else:
            raise ValueError(f"Unsupported configuration file format: {config_file.suffix}")
    
    def update_rules(self, rules: List[Rule]) -> None:
        """
        Update guardrails rules.
        
        Args:
            rules: New list of rules
        """
        self.rules = rules.copy()
        
    def add_rule(self, rule: Rule) -> None:
        """
        Add a new rule.
        
        Args:
            rule: Rule to add
        """
        # Update existing rule if name matches
        for i, existing_rule in enumerate(self.rules):
            if existing_rule.name == rule.name:
                self.rules[i] = rule
                return
                
        self.rules.append(rule)
    
    def remove_rule(self, rule_name: str) -> bool:
        """
        Remove a rule by name.
        
        Args:
            rule_name: Name of the rule to remove
            
        Returns:
            True if rule was removed, False if not found
        """
        for i, rule in enumerate(self.rules):
            if rule.name == rule_name:
                del self.rules[i]
                return True
        return False
    
    def get_rule(self, rule_name: str) -> Optional[Rule]:
        """
        Get a specific rule by name.
        
        Args:
            rule_name: Name of the rule
            
        Returns:
            Rule object if found, None otherwise
        """
        for rule in self.rules:
            if rule.name == rule_name:
                return rule
        return None
    
    def get_rules(self) -> List[Rule]:
        """
        Get all rules.
        
        Returns:
            List of all rules
        """
        return self.rules.copy()
    
    def get_enabled_rules(self) -> List[Rule]:
        """
        Get all enabled rules.
        
        Returns:
            List of enabled rules
        """
        return [rule for rule in self.rules if rule.enabled]
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "version": "1.0",
            "name": "Nvidia NeMo Guardrails",
            "description": "Default configuration for AI safety guardrails",
            "settings": {
                "max_content_length": 10000,
                "safety_threshold": 0.8,
                "enable_logging": True,
                "log_level": "INFO"
            },
            "rules": [
                {
                    "name": "content_safety",
                    "description": "Basic content safety check",
                    "enabled": True,
                    "threshold": 0.8,
                    "parameters": {
                        "harmful_keywords": ["harmful", "dangerous", "illegal", "inappropriate"]
                    }
                },
                {
                    "name": "length_check",
                    "description": "Check content length",
                    "enabled": True,
                    "threshold": 0.9,
                    "parameters": {
                        "max_length": 10000
                    }
                }
            ]
        }
    
    def _load_rules_from_config(self) -> List[Rule]:
        """Load rules from configuration dictionary."""
        rules = []
        config_rules = self.config.get('rules', [])
        
        for rule_config in config_rules:
            rule = Rule(
                name=rule_config['name'],
                description=rule_config['description'],
                enabled=rule_config.get('enabled', True),
                threshold=rule_config.get('threshold', 0.8),
                parameters=rule_config.get('parameters', {})
            )
            rules.append(rule)
            
        return rules
    
    def _rule_to_dict(self, rule: Rule) -> Dict[str, Any]:
        """Convert rule to dictionary for serialization."""
        return {
            "name": rule.name,
            "description": rule.description,
            "enabled": rule.enabled,
            "threshold": rule.threshold,
            "parameters": rule.parameters or {},
            "created_at": rule.created_at.isoformat() if rule.created_at else None,
            "updated_at": rule.updated_at.isoformat() if rule.updated_at else None
        } 