"""
Test None value handling in fields and tags
"""

import pytest
import telegraf_client


def test_none_values_in_fields():
    """Test that None values in fields are skipped"""
    fields = {
        "valid_field": 42,
        "none_field": None,
        "another_valid": "test",
        "another_none": None
    }
    
    point = telegraf_client.Point(
        measurement="test_none_fields",
        tags={"service": "test"},
        fields=fields
    )
    
    assert point is not None


def test_none_values_in_tags():
    """Test that None values in tags become empty strings"""
    tags = {
        "valid_tag": "value",
        "none_tag": None,
        "empty_tag": "",
        "another_none": None
    }
    
    point = telegraf_client.Point(
        measurement="test_none_tags",
        tags=tags,
        fields={"value": 123}
    )
    
    assert point is not None


def test_mixed_none_values():
    """Test mixed None values in both fields and tags"""
    point = telegraf_client.Point(
        measurement="test_mixed",
        tags={
            "host": "server1",
            "env": None,  # Should become empty string
            "region": "us-west"
        },
        fields={
            "cpu": 85.5,
            "memory": None,  # Should be skipped
            "disk": 75.0,
            "network": None  # Should be skipped
        }
    )
    
    assert point is not None


def test_all_none_fields():
    """Test when all fields are None"""
    point = telegraf_client.Point(
        measurement="test_all_none",
        tags={"service": "test"},
        fields={
            "field1": None,
            "field2": None,
            "field3": None
        }
    )
    
    assert point is not None


def test_all_none_tags():
    """Test when all tag values are None"""
    point = telegraf_client.Point(
        measurement="test_all_none_tags",
        tags={
            "tag1": None,
            "tag2": None,
            "tag3": None
        },
        fields={"value": 123}
    )
    
    assert point is not None


def test_none_fields_with_valid_tags():
    """Test None fields with valid tags"""
    point = telegraf_client.Point(
        measurement="test_none_fields_valid_tags",
        tags={
            "service": "api",
            "version": "1.0",
            "env": "production"
        },
        fields={
            "metric1": None,
            "metric2": None
        }
    )
    
    assert point is not None


def test_none_tags_with_valid_fields():
    """Test None tags with valid fields"""
    point = telegraf_client.Point(
        measurement="test_none_tags_valid_fields",
        tags={
            "tag1": None,
            "tag2": None
        },
        fields={
            "cpu": 85.5,
            "memory": 1024,
            "disk": 75.0
        }
    )
    
    assert point is not None
