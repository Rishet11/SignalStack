import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard';
import Opportunities from './pages/Opportunities';
import TickerDetail from './pages/TickerDetail';
import AuditTrail from './pages/AuditTrail';
import './styles/index.css';
import './styles/animations.css';
import './styles/components.css';

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/opportunities" element={<Opportunities />} />
          <Route path="/ticker/:symbol" element={<TickerDetail />} />
          <Route path="/audit/:requestId" element={<AuditTrail />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;
