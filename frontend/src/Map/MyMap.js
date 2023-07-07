import React, { Component } from "react";
import { Map, GoogleApiWrapper, Marker } from "google-maps-react";

class MyMap extends Component {
  constructor(props) {
    super(props);

    this.state = {
      markerPosition: { lat: null, lng: null },
    };

    this.mapRef = React.createRef();
  }

  changeMap = (latitude, longitude) => {
    this.setState(
      {
        markerPosition: {
          lat: latitude,
          lng: longitude,
        },
        currentLocation: {
          lat: latitude,
          lng: longitude,
        },
      }
      // () => {
      //   console.log(this.state.markerPosition);
      //   console.log(this.state.currentLocation);
      // }
    );
  };

  render() {
    const mapStyles = {
      position: "relative",
      width: "100%",
      height: "250px",
    };

    return (
      <Map
        google={this.props.google}
        zoom={12}
        style={mapStyles}
        initialCenter={{ lat: 34.0522, lng: -118.2437 }}
        onChangeMap={this.changeMap}
        ref={this.props.mapRef}
      >
        <Marker position={this.state.markerPosition} />
      </Map>
    );
  }
}

export default GoogleApiWrapper({
  apiKey: "AIzaSyBw3yzPA6bW6zlPT630IDeNs654fVIiggA",
})(MyMap);
