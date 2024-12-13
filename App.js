import React, {useState} from "react";
import "./App.css";

function App(){
  const [degree, setDegree] = useState("");
  const [dataPoints, setDataPoints] = useState("");
  const [results, setResults] = useState(null);
  const API_URL = "https://polynomial-regression-for-co2emission-1.onrender.com/predict";
  const handleSubmit = async (e) => {e.preventDefault();
                                     const requestData = {
                                       degree: parseInt(degree),
                                       data_points: JSON.parse(dataPoints),
                                       try {
                                         const response = await fetch(API_URL,{
                                           method:"POST",
                                           headers: {"Content-Type": "application/json"},
                                           body: JSON.stringify(requestData),
                                         });
                                       if (!response.ok) {
                                         throw new Error("Failed to fetch predictions");
                                       }
                                       const result = await response.json();
                                       setResults(result);
                                     }
                                    };
  return (
    <div className="App">
      <h1>Polynomial Regression Test Interface</h1>
      <form onSubmit = {handleSubmit}>
        <label>Polynomial Degree:
          type:"number"
          value:{degree}
          onChange={(e) => setDegree(e.target.value)} required/>
        </label>
        <br />
        <label>
            Data Points (JSON Format):
            <textarea
              value = {dataPoints}
              onChange={(e) => setDataPoints(e.target.value)}
              placeholder = "Example:[[1,2],[2,4],[3,6]]" required/>
        </label>
        <br />
        <button type="submit">Get Results</button>
      </form>
      {results && (
        <div>
          <h2>Results</h2>
          <p><strong>Equation:</strong>{results.equation}</p>
          <p><strong>Prediction:</strong>{JSON.stringify(results.predictions)}</p>
        </div>
       )}
    </div>
  );
}
export default App
                                       
