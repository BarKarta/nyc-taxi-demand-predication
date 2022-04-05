import React from "react";
import ReactNYC from "react-nyc-choropleth";

const App = (props) => {
  const mapboxAccessToken =
    "pk.eyJ1IjoiYmFya2FydGExIiwiYSI6ImNsMTI2ZXh6NzAwMHIzb210am5xenN2dTUifQ.7otIOgSNLp8uAdGFTdRpOw"; // Your access token
  const mapboxType = "streets";
  const position = [40.7831, -73.9712];
  const zoom = 12;
  const data = props.data;
  const neighborhoodStyle = {
    weight: 1,
    opacity: 1,
    color: "#666",
    dashArray: "3",
    fillOpacity: 0.7,
  };
  const neighborhoodHoverStyle = {
    weight: 5,
    color: "#FFF",
    dashArray: "1",
    fillOpacity: 0.7,
  };
  const excludeNeighborhoods = ["Liberty Island", "Ellis Island"];

  return (
    <div>
      <ReactNYC
        mapboxAccessToken={mapboxAccessToken} // Required
        mapHeight="800px" // Required
        mapWidth="600px"
        className="container"
        mapboxType={mapboxType}
        mapCenter={position}
        mapZoom={zoom}
        mapScrollZoom={false}
        neighborhoodOn={true}
        tooltip={true}
        tooltipSticky={false}
        data={data}
        neighborhoodStyle={neighborhoodStyle}
        neighborhoodHoverStyle={neighborhoodHoverStyle}
        excludeNeighborhoods={excludeNeighborhoods}
      />
    </div>
  );
};

export default App;
