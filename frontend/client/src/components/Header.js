import React from "react";
import { Menu } from "semantic-ui-react";
import { Link } from "react-router-dom";
import GoogleAuth from "./GoogleAuth";

const Header = () => {
  return (
    <Menu>
      <Menu.Item>
        <Link to="/">Streamer</Link>
      </Menu.Item>
      <Menu.Menu position="right">
        <Menu.Item>
          <Link to="/">All Streams</Link>
        </Menu.Item>
        <GoogleAuth />
      </Menu.Menu>
    </Menu>
  );
};
export default Header;
