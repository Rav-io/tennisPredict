import './App.css'
import Home from "./components/Home"
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import GlickoHistory from './components/GlickoHistory';
import EloHistory from './components/EloHistory';
import Layout from './components/Layout';
 
function App() {
  return (
      <Router>
        <Layout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/glicko-history" element={<GlickoHistory />} />
              <Route path="/elo-history" element={<EloHistory />} />
            </Routes>
          </Layout>
      </Router>
  );
}
 
export default App