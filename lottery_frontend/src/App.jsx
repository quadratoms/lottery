
import Home from '../../lottery_frontend1/src/pages/Home';
import Play from '../../lottery_frontend1/src/pages/Play';
import Results from '../../lottery_frontend1/src/pages/Results';
import Wallet from '../../lottery_frontend1/src/pages/Wallet';
import Tickets from '../../lottery_frontend1/src/pages/Tickets';
import Profile from '../../lottery_frontend1/src/pages/Profile';
import Auth from '../../lottery_frontend1/src/pages/Auth';
import TestComponent from '../../lottery_frontend1/src/components/TestComponent';
import Layout from '../../lottery_frontend1/src/components/Layout';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';


function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/play" element={<Play />} />
          <Route path="/results" element={<Results />} />
          <Route path="/wallet" element={<Wallet />} />
          <Route path="/tickets" element={<Tickets />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/auth" element={<Auth />} />
          <Route path="/test" element={<TestComponent />} /> {/* Add a route for TestComponent */}
        </Routes>
      </Layout>
    </Router>
  );
}

export default App
