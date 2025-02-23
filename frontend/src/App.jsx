
import { useState } from "react";
import axios from "axios";

function App() {
  const [formData, setFormData] = useState({
    Age: "",
    Income: "",
    MaritalStatus: "Single",
    NumChildren: "",
    AgeChild1: "",
    AgeChild2: ""
  });

  const [predictions, setPredictions] = useState(null);
  const [error, setError] = useState(null);

  // Handle input changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setPredictions(null);

    // Convert inputs to the correct data types
    const userInput = {
      Age: parseInt(formData.Age),
      Income: parseFloat(formData.Income),
      MaritalStatus: formData.MaritalStatus, 
      NumChildren: parseInt(formData.NumChildren) || 0,  // Default to 0 if empty
      AgeChild1: parseFloat(formData.AgeChild1) || 0.0,   // Default to 0 if empty
      AgeChild2: parseFloat(formData.AgeChild2) || 0.0    // Default to 0 if empty
    };

    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", userInput);
      setPredictions(response.data);
    } catch (err) {
      setError("Error: Could not fetch predictions. Check server logs.");
      console.error("Prediction error:", err);
    }
  };

  return (
    <div className="container">
      <h1>Insurance Plan Predictor</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Age:
          <input type="number" name="Age" value={formData.Age} onChange={handleChange} required />
        </label>

        <label>
          Income (LPA):
          <input type="number" step="0.01" name="Income" value={formData.Income} onChange={handleChange} required />
        </label>

        <label>
          Marital Status:
          <select name="MaritalStatus" value={formData.MaritalStatus} onChange={handleChange}>
            <option value="Single">Single</option>
            <option value="Married">Married</option>
          </select>
        </label>

        <label>
          Number of Children:
          <input type="number" name="NumChildren" value={formData.NumChildren} onChange={handleChange} />
        </label>

        <label>
          Age of Child 1:
          <input type="number" step="0.1" name="AgeChild1" value={formData.AgeChild1} onChange={handleChange} />
        </label>

        <label>
          Age of Child 2:
          <input type="number" step="0.1" name="AgeChild2" value={formData.AgeChild2} onChange={handleChange} />
        </label>

        <button type="submit">Predict Best Plans</button>
      </form>

      {error && <p className="error">{error}</p>}

      {predictions && (
        <div className="results">
          <h2>Recommended Plans</h2>
          <p><strong>Best Plan 1:</strong> {predictions["Best Plan 1"]}</p>
          <p><strong>Best Plan 2:</strong> {predictions["Best Plan 2"]}</p>
        </div>
      )}
    </div>
  );
}

export default App;

