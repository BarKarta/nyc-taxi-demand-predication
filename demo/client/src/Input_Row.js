import "./input_rows.css";
import axios from "axios";

const [zone, setZone] = useState("");
const [date, setDate] = useState("");
const [time, setTime] = useState("");
const bodyFormData = new FormData();
const Input_Row = (props) => {
  const handleSubmit = (event) => {
    event.preventDefault();
    bodyFormData.append("zone", zone);
    bodyFormData.append("date", date);
    bodyFormData.append("time", time);
    axios({
      method: "post",
      url: "http://localhost:5000/calc",
      headers: { "Content-Type": "multipart/form-data" },
    })
      .then(
        (res = () => {
          console.log(res);
        })
      )
      .catch(
        (res = () => {
          console.log(res);
        })
      );
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="input_rows">
        <label for="zone">Zone:</label>
        <input
          type="text"
          value={zone}
          placeholder="Zone"
          onChange={(e) => setZone(e.target.value)}
        />
        <label for="date">Date:</label>
        <input
          type="text"
          value={date}
          placeholder="Date"
          onChange={(e) => setDate(e.target.value)}
        />
        <label for="">Time:</label>
        <input
          type="text"
          value={time}
          placeholder="Time"
          onChange={(e) => setTime(e.target.value)}
        />
        <input type="submit" value="Submit" />
      </div>
    </form>
  );
};
export default Input_Row;
