import React, { useState } from 'react';
import { ArrowRight, ArrowLeft } from 'lucide-react';
import { adCampaigns } from '../data/questions';
import GatedResult from './GatedResult';
import SetlistBuilder from './SetlistBuilder';

export default function Funnel({ campaignId }) {
  const campaign = adCampaigns[campaignId];
  const [started, setStarted] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showSetlistBuilder, setShowSetlistBuilder] = useState(false);
  const [selectedSongs, setSelectedSongs] = useState([]);
  const [showGatedResult, setShowGatedResult] = useState(false);

  const handleStart = () => {
    setStarted(true);
  };

  const handleOptionSelect = (qId, optionValue) => {
    setAnswers(prev => ({ ...prev, [qId]: optionValue }));
    
    // Auto-advance after a short delay
    setTimeout(() => {
      setCurrentStep(prev => {
        if (prev < campaign.questions.length - 1) {
          return prev + 1;
        } else {
          setShowSetlistBuilder(true);
          return prev;
        }
      });
    }, 400);
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    } else {
      setStarted(false);
    }
  };

  const handleBackFromSetlist = () => {
    setShowSetlistBuilder(false);
  };

  const handleSetlistComplete = (songs) => {
    setSelectedSongs(songs);
    setShowSetlistBuilder(false);
    setShowGatedResult(true);
  };

  if (showGatedResult) {
    return <GatedResult answers={answers} campaignSource={campaignId} selectedSongs={selectedSongs} />;
  }

  const currentQuestion = campaign.questions[currentStep];

  return (
    <div className="flex-grow flex flex-col items-center justify-center px-container-padding-mobile md:px-container-padding-desktop py-stack-lg relative w-full">
      
      {!started ? (
        // Entry Hero Section
        <section className="w-full max-w-container-max flex flex-col items-center text-center space-y-stack-md relative z-10 slide-up-enter-active">
          <div className="max-w-2xl mx-auto space-y-stack-sm">
            <h2 className="font-display-lg-mobile md:font-display-lg text-display-lg-mobile md:text-display-lg text-on-surface">
              {campaign.title}
            </h2>
            <p className="font-body-lg text-body-lg text-on-surface-variant max-w-xl mx-auto">
              {campaign.subtitle}
            </p>
          </div>
          <div className="pt-stack-sm pb-stack-sm w-full max-w-md mx-auto">
            <button 
              onClick={handleStart}
              className="w-full sm:w-auto px-8 py-4 bg-primary-container text-on-primary-container rounded-full font-label-caps text-label-caps shadow-ambient hover:-translate-y-1 hover:shadow-glow transition-all duration-300 active:scale-95 group flex items-center justify-center gap-2 mx-auto uppercase"
            >
              Start Assessment
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" />
            </button>
          </div>
          <div className="flex items-center justify-center gap-2 text-on-surface-variant/80 font-label-caps text-label-caps mt-stack-md pt-stack-md border-t border-surface-variant/50 w-full max-w-md mx-auto uppercase">
            <span>10+ Years Expert Mentorship</span>
            <span className="mx-2 opacity-50">•</span>
            <span>500+ Students Forged</span>
          </div>
        </section>
      ) : showSetlistBuilder ? (
        <SetlistBuilder 
          onComplete={handleSetlistComplete} 
          onBack={handleBackFromSetlist} 
        />
      ) : (
        // Interactive Assessment Section
        <section className="w-full max-w-[600px] flex flex-col items-center relative z-10 slide-in-right">
          {/* Progress Bar */}
          <div className="w-full mb-stack-md px-4">
            <div className="flex justify-between items-center mb-2">
              <span className="font-label-caps text-label-caps text-on-surface-variant uppercase">
                Step {currentStep + 1} of {campaign.questions.length}
              </span>
            </div>
            <div className="h-1 w-full bg-surface-variant rounded-full overflow-hidden">
              <div 
                className="h-full bg-primary-container rounded-full transition-all duration-700 ease-out shadow-[0_0_10px_rgba(0,245,160,0.8)]"
                style={{ width: `${((currentStep + 1) / campaign.questions.length) * 100}%` }}
              ></div>
            </div>
          </div>

          {/* Question Card */}
          <div className="w-full bg-surface-container rounded-xl p-stack-md md:p-stack-lg shadow-ambient border border-surface-variant relative">
            <h3 className="font-headline-sm text-headline-sm text-on-surface mb-stack-md text-center">
              {currentQuestion.title}
            </h3>
            
            <div className="flex flex-col gap-stack-sm w-full">
              {currentQuestion.options.map((option, index) => {
                const isSelected = answers[currentQuestion.id] === option.value;
                return (
                  <button 
                    key={index}
                    onClick={() => handleOptionSelect(currentQuestion.id, option.value)}
                    className={`assessment-option group relative w-full text-left p-4 md:p-6 rounded-lg border transition-all duration-300 hover:-translate-y-0.5 focus:outline-none flex items-center gap-4 ${
                      isSelected 
                        ? 'border-primary-container bg-surface-bright shadow-[0_0_15px_rgba(0,245,160,0.15)]' 
                        : 'border-surface-variant bg-surface hover:bg-surface-bright hover:border-primary-container/50 hover:shadow-[0_0_15px_rgba(0,245,160,0.15)]'
                    }`}
                  >
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-colors duration-300 flex-shrink-0 ${
                      isSelected ? 'bg-primary-container/20 text-primary-container' : 'bg-surface-variant text-on-surface-variant group-hover:bg-primary-container/20 group-hover:text-primary-container'
                    }`}>
                      {option.value}
                    </div>
                    <span className="font-body-md text-body-md text-on-surface font-medium relative z-10">
                      {option.label}
                    </span>
                  </button>
                );
              })}
            </div>

            <div className="mt-stack-md pt-stack-sm flex justify-center">
              <button 
                onClick={handleBack}
                className="text-on-surface-variant hover:text-primary-container transition-colors font-label-caps text-label-caps flex items-center gap-1 opacity-80 hover:opacity-100 uppercase tracking-widest"
              >
                <ArrowLeft className="w-4 h-4" /> Back
              </button>
            </div>
          </div>
        </section>
      )}

      {/* Atmospheric background element */}
      <div className="absolute inset-0 -z-10 w-full h-full pointer-events-none overflow-hidden flex items-center justify-center opacity-20">
        <div className="w-[800px] h-[800px] bg-primary-container rounded-full blur-[120px] absolute -top-1/4 -right-1/4 mix-blend-screen opacity-30"></div>
        <div className="w-[600px] h-[600px] bg-secondary-container rounded-full blur-[120px] absolute -bottom-1/4 -left-1/4 mix-blend-screen opacity-20"></div>
      </div>
    </div>
  );
}
