import "./input_rows.css";
import axios from "axios";

const Input_Row = (props) => {
  const handleSubmit = (event) => {
    event.preventDefault();
    axios
      .get("http://localhost:5000/books")
      .then((response) => {
        console.log(response.data);
        props.set_data(response.data);
      })
      .catch((err) => console.log(err));
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="input_rows">
        <label for="zone">zone:</label>
        <input type="text" id="zoneID" />
        <label for="Time">Time:</label>
        <input type="text" id="timeID" />
        <label for="">zone:</label>
        <input type="text" id="zoneID" />
        <label for="zone">zone:</label>
        <input type="text" id="zoneID" />
        <label for="zone">zone:</label>
        <input type="text" id="zoneID" />
        <label for="zone">zone:</label>
        <input type="text" id="zoneID" />
        <label for="zone">zone:</label>
        <input type="text" id="zoneID" />
        <input type="submit" value="Submit" />
      </div>
    </form>
  );
};
export default Input_Row;
