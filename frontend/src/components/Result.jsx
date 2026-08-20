import React from 'react';
import { Calendar, Download } from 'lucide-react';

export default function Result({ data }) {
  const { score_details, result } = data;
  const isQualified = score_details.is_qualified;

  // Split content by bullet points to render them nicely
  const contentParts = result.content.split('\n- ');
  const intro = contentParts[0];
  const bullets = contentParts.slice(1);

  return (
    <div className="flex-grow flex flex-col items-center justify-center px-container-padding-mobile md:px-container-padding-desktop py-stack-lg relative w-full slide-up-enter-active">
      <section className="w-full max-w-[800px] flex flex-col items-center relative z-10">
        
        <div className="text-center mb-stack-lg">
          <h2 className="font-display-lg-mobile md:font-display-lg text-display-lg-mobile md:text-display-lg text-on-surface mb-4">
            {result.title}
          </h2>
          <div className="inline-block bg-surface-variant/50 border border-primary-container/30 px-6 py-2 rounded-full font-label-caps text-label-caps text-primary-container uppercase tracking-widest">
            Profile Match: {score_details.total_score} Points
          </div>
        </div>

        <div className="w-full bg-surface-container rounded-xl p-stack-md md:p-stack-lg shadow-ambient border border-surface-variant relative mb-stack-lg text-left">
          <div className="space-y-4 mb-6">
            {intro.split('\n\n').map((paragraph, idx) => (
              <p key={idx} className="font-body-lg text-body-lg text-on-surface leading-relaxed">
                {paragraph}
              </p>
            ))}
          </div>
          
          <div className="space-y-4">
            {bullets.map((bullet, idx) => {
              const [boldPart, rest] = bullet.split(': ');
              return (
                <div key={idx} className="flex gap-4 items-start bg-surface/50 p-4 rounded-lg border border-surface-variant/50">
                  <div className="w-2 h-2 mt-2 rounded-full bg-primary-container flex-shrink-0"></div>
                  <p className="font-body-md text-on-surface">
                    {rest ? (
                      <><span className="font-bold text-primary-container">{boldPart}: </span>{rest}</>
                    ) : (
                      bullet
                    )}
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Dynamic CTA based on qualification */}
        <div className="w-full max-w-[500px]">
          {isQualified ? (
            <div className="bg-surface-bright border border-secondary p-8 rounded-xl text-center shadow-glow">
              <h3 className="font-headline-sm text-headline-sm text-on-surface mb-2">Ready to accelerate your progress?</h3>
              <p className="font-body-md text-on-surface-variant mb-6">Book a free 1-on-1 strategy call to map out your exact practice routine.</p>
              <button className="w-full px-8 py-4 bg-secondary text-on-secondary rounded-full font-label-caps text-label-caps shadow-ambient hover:-translate-y-1 hover:shadow-glow transition-all duration-300 active:scale-95 flex items-center justify-center gap-2 uppercase">
                <Calendar className="w-5 h-5" /> Book Consultation
              </button>
            </div>
          ) : (
            <div className="bg-surface-bright border border-surface-variant p-8 rounded-xl text-center">
              <h3 className="font-headline-sm text-headline-sm text-on-surface mb-2">Your Free Starter Pack</h3>
              <p className="font-body-md text-on-surface-variant mb-6">We've compiled a set of free resources tailored to your current level.</p>
              <button className="w-full px-8 py-4 bg-surface text-primary-container border border-primary-container rounded-full font-label-caps text-label-caps hover:bg-primary-container/10 transition-all duration-300 active:scale-95 flex items-center justify-center gap-2 uppercase">
                <Download className="w-5 h-5" /> Get Free Resources
              </button>
            </div>
          )}
        </div>

      </section>

      {/* Atmospheric background */}
      <div className="absolute inset-0 -z-10 w-full h-full pointer-events-none overflow-hidden flex items-center justify-center opacity-20">
        <div className="w-[800px] h-[800px] bg-primary-container rounded-full blur-[120px] absolute -top-1/4 -right-1/4 mix-blend-screen opacity-20"></div>
        <div className="w-[600px] h-[600px] bg-secondary-container rounded-full blur-[120px] absolute -bottom-1/4 -left-1/4 mix-blend-screen opacity-10"></div>
      </div>
    </div>
  );
}
