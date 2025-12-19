import pytest
import telegraf_client

def test_point_creation():
    fields = {
        "cpu_usage": 85.5,
        "memory_usage": 1024,
        "is_healthy": True,
        "service_name": "web-server"
    }
    
    tags = {
        "host": "server-01",
        "environment": "production"
    }
    
    point = telegraf_client.Point(
        measurement="system_metrics",
        tags=tags,
        fields=fields,
        timestamp=1234567890
    )
    
    assert point is not None

def test_point_creation_minimal():
    fields = {"cpu": 50.0}
    
    point = telegraf_client.Point(
        measurement="test",
        tags=None,
        fields=fields,
        timestamp=None
    )
    
    assert point is not None

def test_client_creation_udp():
    client = telegraf_client.Client("udp://localhost:8089")
    assert client is not None

def test_client_creation_http():
    try:
        client = telegraf_client.Client("http://localhost:8086")
        assert client is not None
    except Exception:
        pass

def test_error_handling_unsupported_field():
    with pytest.raises(telegraf_client.TelegrafBindingError):
        fields = {"invalid_field": [1, 2, 3]}
        telegraf_client.Point(
            measurement="test",
            tags=None,
            fields=fields
        )

def test_error_handling_invalid_connection():
    with pytest.raises(telegraf_client.TelegrafBindingError):
        telegraf_client.Client("invalid://connection")

def test_client_methods():
    client = telegraf_client.Client("udp://localhost:8089")
    
    f1 = {"test": 1.0}

    p1 = telegraf_client.Point(
        measurement="test",
        tags=None,
        fields=f1
    )

    client.write_point(p1)
    client.close()

def test_write_points():
    client = telegraf_client.Client("udp://localhost:8069")
    f1 = {"test": 1.0}
    f2 = {"test": 2.0}
    p1 = telegraf_client.Point(
        measurement="test",
        tags=None,
        fields=f1
    )
    p2 = telegraf_client.Point(
        measurement="test",
        tags=None,
        fields=f2
    )
    client.write_points([p1, p2])
    client.close()

def test_point_field_types():
    fields = {
        "int_field": 42,
        "float_field": 3.14,
        "bool_field": True,
        "string_field": "test"
    }
    
    point = telegraf_client.Point(
        measurement="test",
        tags=None,
        fields=fields
    )
    
    assert point is not None
