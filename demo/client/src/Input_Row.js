import "./input_rows.css";
const Input_Row = (props) => {
  const handleSubmit = (event) => {
    event.preventDefault();
    props.set_data([
      {
        name: "Chelsea",
        values: [
          { label: "Population", val: 20000 },
          { label: "Restaurants", val: "690" },
        ],
        color: "#E31A1C",
      },
    ]);
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
