import './App.css'
import { Routes, Route, Navigate } from 'react-router-dom'
import React from 'react'

import { Header } from './components'
import { Main, SingleCard } from './pages'
import 'bootstrap/dist/css/bootstrap.min.css';
import './fonts/fonts/Roboto.css';


function App() {
  const loadSingleItem = ({ id, callback }) => {
    setTimeout((_) => {
      callback();
    }, 3000);
  };

  return (
    <div className="App">
      <Header />
      <Routes >
        <Route path="/fpk/:id" element={<SingleCard loadItem={loadSingleItem} />} />
        <Route path="/fpk" element={<Main />} />
        {/* <Route path="/doc" element={<Navigate to="/doc" />} /> */}
      </Routes>
    </div>
  );
}

export default App;
