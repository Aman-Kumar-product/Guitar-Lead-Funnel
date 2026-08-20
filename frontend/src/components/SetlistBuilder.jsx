import React, { useState } from 'react';
import { ArrowRight, ArrowLeft, Music, Check } from 'lucide-react';
import { songsPool } from '../data/songsPool';

export default function SetlistBuilder({ onComplete, onBack }) {
  const [selectedSongs, setSelectedSongs] = useState([]);

  const toggleSong = (songName) => {
    setSelectedSongs(prev => {
      if (prev.includes(songName)) {
        return prev.filter(name => name !== songName);
      }
      if (prev.length < 5) {
        return [...prev, songName];
      }
      return prev;
    });
  };

  return (
    <div className="w-full flex flex-col items-center justify-center relative z-10 slide-up-enter-active max-w-4xl mx-auto py-stack-md">
      <div className="text-center mb-stack-md max-w-2xl px-4">
        <h2 className="font-display-md text-display-md text-on-surface mb-2">
          Pick Your 5 Dream Songs
        </h2>
        <p className="font-body-lg text-body-lg text-on-surface-variant">
          Select exactly 5 songs you'd love to play. We'll use this to customize your roadmap!
        </p>
      </div>

      <div className="mb-stack-md flex items-center justify-center">
        <div className="inline-flex items-center justify-center px-6 py-3 bg-surface-container border border-surface-variant rounded-full shadow-ambient">
          <Music className="w-5 h-5 mr-3 text-primary-container" />
          <span className="font-label-lg text-label-lg text-on-surface">
            {selectedSongs.length} / 5 Selected
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-stack-lg w-full px-4">
        {songsPool.map((song, index) => {
          const isSelected = selectedSongs.includes(song.name);
          const isDisabled = !isSelected && selectedSongs.length >= 5;
          
          return (
            <button
              key={index}
              onClick={() => toggleSong(song.name)}
              disabled={isDisabled}
              className={`p-4 rounded-xl border text-left transition-all duration-300 flex flex-col justify-between h-28 relative overflow-hidden ${
                isSelected
                  ? 'border-primary-container bg-primary-container/10 shadow-[0_0_15px_rgba(0,245,160,0.15)] scale-[1.02]'
                  : 'border-surface-variant bg-surface-container hover:border-primary-container/50 hover:bg-surface-bright'
              } ${isDisabled ? 'opacity-40 cursor-not-allowed grayscale' : ''}`}
            >
              <span className={`font-body-md text-body-md font-medium line-clamp-2 relative z-10 ${isSelected ? 'text-primary-container font-semibold' : 'text-on-surface'}`}>
                {song.name}
              </span>
              
              <div className="flex justify-end items-end relative z-10 mt-2">
                <div className={`w-6 h-6 rounded-full flex items-center justify-center border transition-colors ${
                  isSelected 
                    ? 'bg-primary-container border-primary-container text-on-primary-container' 
                    : 'border-surface-variant text-transparent'
                }`}>
                  <Check className="w-4 h-4" />
                </div>
              </div>
              
              {isSelected && (
                <div className="absolute inset-0 bg-gradient-to-tr from-primary-container/5 to-transparent pointer-events-none" />
              )}
            </button>
          );
        })}
      </div>

      <div className="flex flex-col items-center justify-center gap-6 w-full mt-4">
        <button
          onClick={() => onComplete(selectedSongs)}
          disabled={selectedSongs.length !== 5}
          className={`px-8 py-4 rounded-full font-label-caps text-label-caps uppercase flex items-center gap-2 transition-all duration-300 ${
            selectedSongs.length === 5
              ? 'bg-primary-container text-on-primary-container hover:-translate-y-1 hover:shadow-glow active:scale-95'
              : 'bg-surface-variant text-on-surface-variant/50 cursor-not-allowed'
          }`}
        >
          Build My Guitar Roadmap
          <ArrowRight className="w-5 h-5" />
        </button>
        
        <button 
          onClick={onBack}
          className="text-on-surface-variant hover:text-primary-container transition-colors font-label-caps text-label-caps flex items-center gap-1 opacity-80 hover:opacity-100 uppercase tracking-widest"
        >
          <ArrowLeft className="w-4 h-4" /> Back
        </button>
      </div>
    </div>
  );
}
