import React from "react";
import { useLocation, Link, useNavigate } from "react-router-dom";
import { Button, Typography } from "@mui/material";
import Box from "@mui/material/Box";

const Nav = () => {
  console.log("Nav render");
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <nav
      style={{
        display: "flex",
        alignItems: "center",
        paddingBottom: 10,
        border: "none",
      }}
    >
      <Typography variant="h6">
        <Link to="/" style={{ textDecoration: "none" }}>
          Knowledge Horizons
        </Link>
      </Typography>
      <div style={{ minWidth: 20 }}></div>
      <Box
        sx={{
          flexGrow: 1,
          color: "red",
          border: "none",
        }}
      >

      </Box>
      <Box sx={{ flexGrow: 0, fontSize: "1em" }}>
          <span>
            <Link
              style={{
                textDecoration: "none",
                color: location.pathname === "/newsletter" ? "#1976d2" : "gray",
                fontWeight:
                  location.pathname === "/newsletter" ? "bold" : "normal",
              }}
              to="/newsletter"
            >Newsletter
            </Link>{" "}
            |{" "}
            <Link
              style={{
                textDecoration: "none",
                color: location.pathname === "/workbench" ? "#1976d2" : "gray",
                fontWeight: location.pathname === "/workbench" ? "bold" : "normal",
              }}
              to="/workbench"
            >
              Workbench
            </Link>{" "}
            </span>
      </Box>
    </nav>
  );
};

export default Nav;
