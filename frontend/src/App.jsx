import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Funnel from './components/Funnel';
import BookingPage from './components/BookingPage';

function Home() {
  return (
    <div className="flex-grow flex flex-col items-center justify-center px-container-padding-mobile md:px-container-padding-desktop py-stack-lg relative w-full">
      <section className="w-full max-w-2xl flex flex-col items-center text-center space-y-stack-md relative z-10">
        <h2 className="font-display-lg-mobile md:font-display-lg text-display-lg-mobile md:text-display-lg text-on-surface mb-8">
          Guitar Academy Entry Points
        </h2>
        <div className="flex flex-col gap-4 w-full max-w-md">
          <Link to="/ad1" className="w-full px-8 py-4 bg-surface-container border border-surface-variant text-on-surface rounded-xl font-headline-sm hover:border-primary-container hover:shadow-glow transition-all">
            Ad 1: Learning Profile Funnel
          </Link>
          <Link to="/ad2" className="w-full px-8 py-4 bg-surface-container border border-surface-variant text-on-surface rounded-xl font-headline-sm hover:border-primary-container hover:shadow-glow transition-all">
            Ad 2: Signature Sound Funnel
          </Link>
          <Link to="/ad3" className="w-full px-8 py-4 bg-surface-container border border-surface-variant text-on-surface rounded-xl font-headline-sm hover:border-primary-container hover:shadow-glow transition-all">
            Ad 3: Timeline Estimator Funnel
          </Link>
        </div>
      </section>

      {/* Atmospheric background */}
      <div className="absolute inset-0 -z-10 w-full h-full pointer-events-none overflow-hidden flex items-center justify-center opacity-20">
        <div className="w-[800px] h-[800px] bg-primary-container rounded-full blur-[120px] absolute -top-1/4 -right-1/4 mix-blend-screen opacity-30"></div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="w-full relative min-h-screen flex flex-col">
        <header className="w-full p-4 md:p-6 z-50 flex justify-center absolute top-0">
          <Link to="/">
            <img src="/logo.png" alt="Logo" className="h-12 md:h-16 w-auto object-contain drop-shadow-md" />
          </Link>
        </header>
        <div className="flex-grow flex flex-col pt-24 md:pt-28">
          <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/ad1" element={<Funnel campaignId="ad_1" />} />
        <Route path="/ad2" element={<Funnel campaignId="ad_2" />} />
        <Route path="/ad3" element={<Funnel campaignId="ad_3" />} />
        <Route path="/book" element={<BookingPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
