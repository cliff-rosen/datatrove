import { Routes, Route } from "react-router-dom";
import { useSessionManager } from "./utils/Auth";
import Main from "./components/Main";
import Container from "@mui/material/Container";

function App() {
  // const sessionManager = useSessionManager();
  const sessionManager = {}

  return (
    <Container>
      <Routes>
        <Route path="/" element={<Main sessionManager={sessionManager} />} />
      </Routes>
    </Container>
  );
}
export default App;
