const Input_Row = () => {
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("hello");
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label for="zone">zone:</label>
        <input type="text" id="zoneID" />
        <br />
        <label for="Time">Time:</label>
        <input type="text" id="timeID" />
        <br />
        <label for="">zone:</label>
        <input type="text" id="zoneID" />
        <br />
        <label for="zone">zone:</label>
        <input type="text" id="zoneID" />
        <br />
        <label for="zone">zone:</label>
        <input type="text" id="zoneID" />
        <br />
        <label for="zone">zone:</label>
        <input type="text" id="zoneID" />
        <br />
        <label for="zone">zone:</label>
        <input type="text" id="zoneID" />
        <br />
        <input type="submit" value="Submit" />
      </form>
    </div>
  );
};
export default Input_Row;
