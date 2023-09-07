// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Nav from './components/Nav';
import Rvr from './page/Rvr';
import Test from './page/Test';
import './App.css'

function App() {
  return (
    <Router>
      <div>
        <header>
          <h1>台灣房產實價登錄</h1>
        </header>
        <Nav />
        <Routes>
          <Route path="/" />
          <Route path="/rvr" element={<Rvr />} />
          <Route path="/test" element={<Test />} />
        </Routes>
        <footer>
          &copy; TKU資工專題(實價登入)
        </footer>
      </div>
    </Router>
  );
}

export default App;
