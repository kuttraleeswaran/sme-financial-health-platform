import React, { useState } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

function Dashboard(){

  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [language, setLanguage] = useState("en");

  const uploadFile = async () => {

    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(
      "http://127.0.0.1:8000/upload",
      formData
    );

    setData(res.data);
  };

  return(
    <div style={styles.container}>

      <h1 style={styles.title}>SME Financial Health AI</h1>

      <div style={styles.controls}>
        <input type="file" onChange={e => setFile(e.target.files[0])} />
        <button style={styles.btn} onClick={uploadFile}>Analyze</button>

        <button 
          style={styles.langBtn}
          onClick={()=> setLanguage(language === "en" ? "hi" : "en")}
        >
          {language === "en" ? "Switch to Hindi" : "English"}
        </button>

        <a 
          href="http://127.0.0.1:8000/download-report" 
          target="_blank"
          rel="noreferrer"
        >
          <button style={styles.pdfBtn}>Download PDF</button>
        </a>
      </div>

      {data && (
        <div style={styles.grid}>

          {/* Health Card */}
          <div style={styles.card}>
            <h2>Health Score</h2>
            <h1 style={{color:"#2ecc71"}}>{data.summary.health_score}</h1>
            <p>Profit Margin: {data.summary.profit_margin}%</p>
          </div>

          {/* Forecast Card */}
          <div style={styles.card}>
            <h2>Revenue Forecast</h2>

            <LineChart width={300} height={200} data={
              data.forecast.map((v,i)=>({month:i+1, revenue:v}))
            }>
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <CartesianGrid />
              <Line dataKey="revenue" />
            </LineChart>
          </div>

          {/* Risk Card */}
          <div style={styles.card}>
            <h2>Risks</h2>
            <ul>
              {data.summary.risks.length === 0 ? 
                <li>No major risks</li> :
                data.summary.risks.map((r,i)=><li key={i}>{r}</li>)
              }
            </ul>
          </div>

          {/* Industry Benchmark */}
          <div style={styles.card}>
            <h2>Industry Benchmark</h2>
            <p><b>Industry:</b> {data.benchmark.industry}</p>
            <p>Your Margin: {data.benchmark.your_profit_margin}%</p>
            <p>Industry Avg: {data.benchmark.industry_profit_margin}%</p>
            <p>Your Score: {data.benchmark.your_health_score}</p>
            <p>Industry Score: {data.benchmark.industry_health_score}</p>
          </div>

          {/* AI Insights */}
          <div style={{...styles.card, gridColumn:"1 / span 2"}}>
            <h2>AI Insights</h2>
            <pre style={{whiteSpace:"pre-wrap"}}>{data.ai_insights}</pre>
          </div>

        </div>
      )}

    </div>
  )
}

export default Dashboard;


const styles = {

  container:{
    padding:"20px",
    fontFamily:"Arial",
    background:"#f4f6f9",
    minHeight:"100vh"
  },

  title:{
    textAlign:"center",
    marginBottom:"20px"
  },

  controls:{
    display:"flex",
    gap:"10px",
    justifyContent:"center",
    marginBottom:"20px"
  },

  btn:{
    background:"#3498db",
    color:"white",
    border:"none",
    padding:"8px 15px",
    cursor:"pointer"
  },

  langBtn:{
    background:"#9b59b6",
    color:"white",
    border:"none",
    padding:"8px 15px",
    cursor:"pointer"
  },

  pdfBtn:{
    background:"#27ae60",
    color:"white",
    border:"none",
    padding:"8px 15px",
    cursor:"pointer"
  },

  grid:{
    display:"grid",
    gridTemplateColumns:"repeat(2, 1fr)",
    gap:"15px"
  },

  card:{
    background:"white",
    padding:"15px",
    borderRadius:"10px",
    boxShadow:"0 2px 8px rgba(0,0,0,0.1)"
  }
};
