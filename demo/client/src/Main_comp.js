import { useState } from "react";
import App from "./App";
import Input_Row from "./Input_Row";
import "./main_comp.css";

const Main_comp = () => {
  const [data, setData] = useState([]);
    
  return (
    <>
      <div className="title">
        <h1>NYC Demo</h1>
      </div>
      <div className="container">
        <Input_Row set_data={setData} />
        <App data={data} />
      </div>
    </>
  );
};
export default Main_comp;
