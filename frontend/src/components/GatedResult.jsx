import React, { useState, useEffect } from 'react';
import { Mail, Loader2 } from 'lucide-react';
import BookingForm from './BookingForm';

export default function GatedResult({ answers, campaignSource, selectedSongs }) {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [partialResult, setPartialResult] = useState(null);
  const [leadData, setLeadData] = useState(null); // When full result is unlocked

  // Fetch partial result on mount
  useEffect(() => {
    const fetchPartialScore = async () => {
      try {
        const payload = { campaign_source: campaignSource, assessment_answers: answers, selected_songs: selectedSongs || [] };
        const response = await fetch(`${import.meta.env.VITE_API_URL || ''}/api/score`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (response.ok) {
          const data = await response.json();
          setPartialResult(data);
        }
      } catch (err) {
        console.error("Error fetching partial score", err);
        setError("Could not load your profile preview, but you can still receive your roadmap! " + err.message);
      }
    };
    fetchPartialScore();
  }, [answers, campaignSource, selectedSongs]);

  const handleSubmitEmail = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const payload = {
      campaign_source: campaignSource,
      email: email,
      assessment_answers: answers,
      selected_songs: selectedSongs || []
    };

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || ''}/api/lead`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error('Failed to unlock result. Please try again.');
      }

      const data = await response.json();
      setLeadData(data); // Unlocks the next step
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (leadData) {
    // Pass the full lead data (which includes lead_id) to the booking form
    return <BookingForm leadData={leadData} />;
  }

  return (
    <div className="flex-grow flex flex-col items-center justify-center px-container-padding-mobile md:px-container-padding-desktop py-stack-lg relative w-full slide-up-enter-active">
      <section className="w-full max-w-[600px] flex flex-col items-center relative z-10">
        
        {/* Partial Result Display */}
        {partialResult && (
          <div className="w-full bg-surface-container-low p-stack-md rounded-2xl shadow-ambient text-center mb-stack-md border border-outline-variant/30">
            <span className="font-label-caps text-label-caps text-primary-container uppercase tracking-widest mb-2 block">Your Playing Profile</span>
            <h2 className="font-headline-md text-headline-md md:text-display-lg-mobile text-primary-container mb-stack-sm font-bold italic shadow-glow">
              {partialResult.title}
            </h2>
            <div className="space-y-4">
              {partialResult.short_content.split('\n\n').map((paragraph, idx) => (
                <p key={idx} className="font-body-lg text-body-md md:text-body-lg text-on-surface-variant">
                  {paragraph}
                </p>
              ))}
            </div>
          </div>
        )}

        {/* Email Capture Form */}
        <div className="w-full bg-primary-container/10 border border-primary-container/50 rounded-2xl p-stack-md text-center shadow-ambient mb-stack-lg">
          <h3 className="font-headline-sm md:font-headline-md text-headline-sm md:text-headline-md text-primary-container mb-4">Get Your Detailed Result via Email</h3>
          <p className="font-body-md text-on-surface-variant mb-6">We've analyzed your profile. Enter your email to receive your personalized 12-week roadmap and song list.</p>
          
          <form onSubmit={handleSubmitEmail} className="flex flex-col gap-4">
            <input 
              type="email" 
              required 
              placeholder="Enter your email address"
              className="w-full bg-surface-container border border-outline-variant/50 rounded-full px-6 py-4 text-on-background focus:border-primary-container outline-none transition-all"
              value={email}
              onChange={e => setEmail(e.target.value)}
            />
            
            {error && <p className="text-error text-sm">{error}</p>}

            <button 
              type="submit" 
              disabled={loading}
              className="w-full bg-primary-container text-on-primary-container font-label-caps text-label-caps py-4 px-8 rounded-full hover:-translate-y-1 transition-all duration-300 flex items-center justify-center gap-2 shadow-glow uppercase disabled:opacity-50"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : (
                <>Send My Detailed Roadmap <Mail className="w-5 h-5" /></>
              )}
            </button>
          </form>
        </div>
      </section>
      
      {/* Background Elements */}
      <div className="absolute inset-0 -z-10 w-full h-full pointer-events-none overflow-hidden flex items-center justify-center opacity-20">
        <div className="w-[800px] h-[800px] bg-primary-container rounded-full blur-[120px] absolute -top-1/4 -right-1/4 mix-blend-screen opacity-30"></div>
      </div>
    </div>
  );
}
