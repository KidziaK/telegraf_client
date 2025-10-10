use pyo3::create_exception;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyModule};
use std::collections::HashMap;
use telegraf::{self, IntoFieldData};

create_exception!(
    telegraf_client,
    TelegrafBindingError,
    pyo3::exceptions::PyException
);

#[pyclass(name = "Point")]
#[derive(Clone)]
struct PyPoint {
    inner: telegraf::Point,
}

#[pymethods]
impl PyPoint {
    #[new]
    #[pyo3(signature = (measurement, tags, fields, timestamp=None))]
    fn new(
        measurement: String,
        tags: Option<HashMap<String, String>>,
        fields: &Bound<'_, PyDict>,
        timestamp: Option<u64>,
    ) -> PyResult<Self> {
        let rust_tags: Vec<(String, String)> = tags.unwrap_or_default().into_iter().collect();
        let mut rust_fields: Vec<(String, Box<dyn IntoFieldData>)> = Vec::new();

        for (key, value) in fields.iter() {
            let key_str = key.extract::<String>()?;
            let field_value: Box<dyn IntoFieldData> = if let Ok(val) = value.extract::<bool>() {
                Box::new(val)
            } else if let Ok(val) = value.extract::<i64>() {
                Box::new(val)
            } else if let Ok(val) = value.extract::<f64>() {
                Box::new(val)
            } else if let Ok(val) = value.extract::<String>() {
                Box::new(val)
            } else {
                let msg = format!("Unsupported field type for key '{}'", key_str);
                return Err(TelegrafBindingError::new_err(msg));
            };
            rust_fields.push((key_str, field_value));
        }

        // Use current timestamp if None is provided
        let final_timestamp = timestamp.unwrap_or_else(|| {
            std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_nanos() as u64
        });
        
        let point = telegraf::Point::new(measurement, rust_tags, rust_fields, Some(final_timestamp));
        Ok(PyPoint { inner: point })
    }
}

#[pyclass(name = "Client", unsendable)]
struct PyClient {
    inner: telegraf::Client,
}

#[pymethods]
impl PyClient {
    #[new]
    fn new(conn_url: &str) -> PyResult<Self> {
        let client = telegraf::Client::new(conn_url)
            .map_err(|e| TelegrafBindingError::new_err(e.to_string()))?;
        Ok(PyClient { inner: client })
    }

    fn write_point(&mut self, point: &Bound<'_, PyPoint>) -> PyResult<()> {
        let py_point_ref: PyRef<'_, PyPoint> = point.borrow();
        self.inner
            .write_point(&py_point_ref.inner)
            .map_err(|e| TelegrafBindingError::new_err(e.to_string()))?;
        Ok(())
    }

    fn close(&self) -> PyResult<()> {
        self.inner
            .close()
            .map_err(|e| TelegrafBindingError::new_err(e.to_string()))?;
        Ok(())
    }

}

#[pymodule]
fn telegraf_client(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyPoint>()?;
    m.add_class::<PyClient>()?;
    m.add(
        "TelegrafBindingError",
        _py.get_type_bound::<TelegrafBindingError>(),
    )?;
    Ok(())
}