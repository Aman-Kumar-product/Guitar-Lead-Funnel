import React, { useState, useEffect } from 'react';
import { Calendar, CheckCircle2, Loader2 } from 'lucide-react';

export default function BookingForm({ leadData, fromEmail = false }) {
  const { lead_id, score_details, email } = leadData;
  const isQualified = score_details.is_qualified;
  
  const [formData, setFormData] = useState({ name: '', phone: '+91 ', timeSlot: '', bot_field: '' });
  const [loading, setLoading] = useState(false);
  const [fetchingSlots, setFetchingSlots] = useState(true);
  const [timeSlots, setTimeSlots] = useState([]);
  const [success, setSuccess] = useState(false);
  const [resultsOnlySuccess, setResultsOnlySuccess] = useState(false);
  const [sendingResults, setSendingResults] = useState(false);
  const [errors, setErrors] = useState({ name: '', phone: '', submit: '' });

  useEffect(() => {
    // Always fetch slots if they are qualified or if they clicked from the email
    if (isQualified || fromEmail) {
      const fetchSlots = async () => {
        try {
          const res = await fetch(`${import.meta.env.VITE_API_URL || ''}/api/available-slots`);
          if (!res.ok) throw new Error('Failed to fetch slots');
          const data = await res.json();
          setTimeSlots(data.slots || []);
          if (data.slots && data.slots.length > 0) {
            setFormData(prev => ({ ...prev, timeSlot: data.slots[0] }));
          }
        } catch (err) {
          console.error(err);
          // Fallback slots on error
          const fallbacks = [
            "Monday, Oct 25 at 10:00 AM - 10:30 AM", 
            "Tuesday, Oct 26 at 2:00 PM - 2:30 PM", 
            "Thursday, Oct 28 at 4:30 PM - 5:00 PM"
          ];
          setTimeSlots(fallbacks);
          setFormData(prev => ({ ...prev, timeSlot: fallbacks[0] }));
        } finally {
          setFetchingSlots(false);
        }
      };
      fetchSlots();
    }
  }, [isQualified, fromEmail]);

  // If they are not qualified AND didn't come from the email link, show success message instead of booking form
  if (!isQualified && !fromEmail) {
    return (
      <div className="flex-grow flex flex-col items-center justify-center px-container-padding-mobile py-stack-lg w-full slide-up-enter-active text-center">
        <div className="bg-surface-container p-8 rounded-2xl shadow-ambient max-w-md border border-primary-container/30">
          <CheckCircle2 className="w-16 h-16 text-primary-container mx-auto mb-4" />
          <h2 className="font-headline-md text-headline-md text-on-surface mb-2">Check Your Inbox!</h2>
          <p className="text-on-surface-variant">We've sent your detailed roadmap and free custom resources tailored to your exact profile. You can also book a free strategy session from the link in your email if you're interested!</p>
        </div>
      </div>
    );
  }

  // If already booked
  if (leadData.booking_status === "Booked" && !success) {
    return (
      <div className="flex-grow flex flex-col items-center justify-center px-container-padding-mobile py-stack-lg w-full slide-up-enter-active text-center">
        <div className="bg-surface-container p-8 rounded-2xl shadow-ambient max-w-md border border-primary-container/30">
          <Calendar className="w-16 h-16 text-primary-container mx-auto mb-4" />
          <h2 className="font-headline-md text-headline-md text-on-surface mb-2">You've already booked your 100% Free Consultation</h2>
          <p className="text-on-surface-variant mb-6">Missed booking?</p>
          <button className="group relative flex items-center justify-center gap-2 bg-primary-container text-on-primary-container font-headline-sm text-headline-sm px-8 py-4 rounded-full shadow-glow hover:-translate-y-1 transition-all duration-300 uppercase w-full">
            Contact Support
          </button>
        </div>
      </div>
    );
  }

  if (success) {
    return (
      <div className="flex-grow flex flex-col items-center justify-center px-container-padding-mobile py-stack-lg w-full slide-up-enter-active text-center">
        <div className="bg-surface-container p-8 rounded-2xl shadow-ambient max-w-md border border-primary-container/30">
          <Calendar className="w-16 h-16 text-primary-container mx-auto mb-4" />
          <h2 className="font-headline-md text-headline-md text-on-surface mb-2">Booking Confirmed</h2>
          <p className="text-on-surface-variant">Your free strategy call is locked in. We will reach out shortly with the calendar invite.</p>
        </div>
      </div>
    );
  }

  if (resultsOnlySuccess) {
    return (
      <div className="flex-grow flex flex-col items-center justify-center px-container-padding-mobile py-stack-lg w-full slide-up-enter-active text-center">
        <div className="bg-surface-container p-8 rounded-2xl shadow-ambient max-w-md border border-primary-container/30">
          <CheckCircle2 className="w-16 h-16 text-primary-container mx-auto mb-4" />
          <h2 className="font-headline-md text-headline-md text-on-surface mb-2">Check Your Inbox!</h2>
          <p className="text-on-surface-variant">We've sent your free custom resources to your email. You can book a session later if you change your mind.</p>
        </div>
      </div>
    );
  }

  const validateFrontend = () => {
    let isValid = true;
    let newErrors = { name: '', phone: '', submit: '' };

    // Name Validation
    const nameVal = formData.name.trim();
    if (nameVal.length < 2) {
      newErrors.name = 'Name must be at least 2 characters long.';
      isValid = false;
    } else if (!/^[A-Za-z\s\-']+$/.test(nameVal)) {
      newErrors.name = 'Name can only contain letters, spaces, hyphens, and apostrophes.';
      isValid = false;
    } else if (['test', 'asdf', 'qwer', 'admin', 'dummy', 'null'].includes(nameVal.toLowerCase())) {
      newErrors.name = 'Please provide a valid name.';
      isValid = false;
    }

    // Phone Validation
    const phoneRaw = formData.phone;
    let digits = phoneRaw.replace(/[\s\-()]/g, '');
    if (digits.startsWith('+91')) digits = digits.slice(3);
    else if (digits.startsWith('91') && digits.length === 12) digits = digits.slice(2);

    if (digits.length !== 10) {
      newErrors.phone = 'Phone number must be exactly 10 digits (excluding +91).';
      isValid = false;
    } else if (new Set(digits).size === 1) {
      newErrors.phone = 'Phone number cannot be all identical digits.';
      isValid = false;
    } else if (['1234567890', '0987654321', '9876543210', '0123456789'].includes(digits)) {
      newErrors.phone = 'Please provide a valid phone number.';
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handlePhoneChange = (e) => {
    let val = e.target.value;
    
    // Ensure +91 prefix is always there
    if (!val.startsWith('+91 ')) {
      // User might have tried to delete it
      if (val === '+91' || val === '+9' || val === '+' || val === '') {
        val = '+91 ';
      } else if (val.startsWith('+91')) {
        val = '+91 ' + val.substring(3).trim();
      } else {
        val = '+91 ' + val;
      }
    }

    // Strip out any non numeric chars after prefix
    const prefix = '+91 ';
    const rest = val.substring(prefix.length).replace(/[^0-9]/g, '');
    // Limit to 10 digits
    const limitedRest = rest.substring(0, 10);
    
    setFormData({ ...formData, phone: prefix + limitedRest });
    if (errors.phone) setErrors({ ...errors, phone: '' });
  };

  const handleNameChange = (e) => {
    setFormData({ ...formData, name: e.target.value });
    if (errors.name) setErrors({ ...errors, name: '' });
  };

  const handleSendResultsOnly = async () => {
    if (!validateFrontend()) return;
    setSendingResults(true);
    
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || ''}/api/send-results-only`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lead_id: lead_id,
          email: email,
          name: formData.name,
          phone: formData.phone
        })
      });
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to send results.');
      }
      setResultsOnlySuccess(true);
    } catch (err) {
      setErrors({ ...errors, submit: err.message });
    } finally {
      setSendingResults(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Bot prevention (Honeypot)
    if (formData.bot_field) {
      // Silently succeed to trick bots
      setSuccess(true);
      return;
    }

    if (!validateFrontend()) return;
    
    setLoading(true);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || ''}/api/book`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lead_id: lead_id,
          name: formData.name,
          phone: formData.phone,
          time_slot: formData.timeSlot,
          email: email
        })
      });

      if (!response.ok) {
        const errData = await response.json();
        if (response.status === 422) {
          // Pydantic validation error
          const msgs = errData.detail.map(e => e.msg).join(", ");
          throw new Error(`Validation Error: ${msgs}`);
        }
        throw new Error(errData.detail || 'Failed to submit booking.');
      }
      
      setSuccess(true);
    } catch (err) {
      setErrors({ ...errors, submit: err.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-grow flex flex-col items-center justify-center px-container-padding-mobile md:px-container-padding-desktop py-stack-lg relative w-full slide-up-enter-active">
      <div className="w-full max-w-3xl bg-surface-container/80 backdrop-blur-md rounded-2xl p-6 md:p-12 border border-surface-variant shadow-ambient relative overflow-hidden">
        
        <div className="relative z-10 flex flex-col items-center text-center mb-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-surface-container-highest rounded-full mb-6 border border-outline-variant">
            <span className="w-2 h-2 rounded-full bg-secondary shadow-[0_0_10px_rgba(255,185,86,0.8)]"></span>
            <span className="font-label-caps text-label-caps text-secondary uppercase">Final Step</span>
          </div>
          <h1 className="font-display-lg-mobile md:font-display-lg text-display-lg-mobile md:text-display-lg text-on-surface mb-4">
            Book Your Free Consultation
          </h1>
          <p className="font-body-lg text-body-lg text-on-surface-variant max-w-xl mx-auto">
            We've emailed your detailed roadmap. Select a time below to discuss your personalized 12-week strategy with an expert.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="relative z-10 space-y-8 w-full" noValidate>
          {/* Honeypot field - visually hidden */}
          <div className="hidden" aria-hidden="true" style={{ display: 'none' }}>
            <label htmlFor="bot_field">Do not fill this out if you are human</label>
            <input 
              type="text" 
              id="bot_field" 
              name="bot_field" 
              value={formData.bot_field}
              onChange={e => setFormData({...formData, bot_field: e.target.value})}
              tabIndex="-1"
              autoComplete="off"
            />
          </div>

          {/* Contact Details */}
          <div className="space-y-4">
            <h2 className="font-headline-sm text-headline-sm text-on-surface mb-2 flex items-center gap-2">
              Contact Details
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="md:col-span-2">
                <label htmlFor="email" className="block font-label-caps text-label-caps text-on-surface-variant mb-2 uppercase">Email Address (Pre-filled)</label>
                <input 
                  type="email" 
                  id="email"
                  className="w-full bg-surface-dim/30 border-b border-outline-variant px-4 py-3 text-on-surface-variant cursor-not-allowed outline-none"
                  value={email}
                  disabled
                  aria-disabled="true"
                />
              </div>
              <div>
                <label htmlFor="fullName" className="block font-label-caps text-label-caps text-on-surface-variant mb-2 uppercase">Full Name</label>
                <input 
                  type="text" 
                  id="fullName"
                  required 
                  className={`w-full bg-surface-dim/50 border-b ${errors.name ? 'border-error focus:border-error' : 'border-outline-variant focus:border-primary-container'} px-4 py-3 text-on-surface placeholder-on-surface-variant/40 outline-none transition-colors`}
                  placeholder="John Doe"
                  value={formData.name}
                  onChange={handleNameChange}
                  aria-invalid={!!errors.name}
                  aria-describedby={errors.name ? "name-error" : undefined}
                />
                {errors.name && <p id="name-error" className="text-error text-sm mt-1">{errors.name}</p>}
              </div>
              <div>
                <label htmlFor="phone" className="block font-label-caps text-label-caps text-on-surface-variant mb-2 uppercase">Phone Number</label>
                <input 
                  type="tel" 
                  id="phone"
                  required 
                  className={`w-full bg-surface-dim/50 border-b ${errors.phone ? 'border-error focus:border-error' : 'border-outline-variant focus:border-primary-container'} px-4 py-3 text-on-surface placeholder-on-surface-variant/40 outline-none transition-colors`}
                  placeholder="+91 "
                  value={formData.phone}
                  onChange={handlePhoneChange}
                  aria-invalid={!!errors.phone}
                  aria-describedby={errors.phone ? "phone-error" : undefined}
                />
                {errors.phone && <p id="phone-error" className="text-error text-sm mt-1">{errors.phone}</p>}
              </div>
            </div>
          </div>

          {/* Time Slots */}
          <div className="space-y-4 pt-4 border-t border-surface-variant">
            <h2 className="font-headline-sm text-headline-sm text-on-surface mb-2">Available Time Slots</h2>
            {fetchingSlots ? (
              <div className="flex items-center justify-center py-8 text-on-surface-variant">
                <Loader2 className="w-8 h-8 animate-spin" />
                <span className="ml-3 font-label-caps">Checking availability...</span>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {timeSlots.map(slot => (
                  <div key={slot} className="relative group">
                    <input 
                      type="radio" name="timeSlot" id={slot} className="peer sr-only"
                      checked={formData.timeSlot === slot}
                      onChange={() => setFormData({...formData, timeSlot: slot})}
                      aria-label={`Select time slot ${slot}`}
                    />
                    <label htmlFor={slot} className="flex flex-col items-center justify-center p-4 bg-surface-container rounded-xl border border-surface-variant cursor-pointer transition-all duration-200 hover:border-outline-variant peer-checked:border-primary-container peer-checked:bg-primary-container/10">
                      <span className="font-label-caps text-label-caps text-on-surface-variant uppercase mb-1 text-center">{slot.split('at')[0]}</span>
                      <span className="font-headline-sm text-headline-sm text-on-surface font-bold peer-checked:text-primary-container text-center">{slot.split('at')[1] || slot}</span>
                    </label>
                  </div>
                ))}
              </div>
            )}
          </div>

          {errors.submit && <p className="text-error text-center font-medium bg-error/10 py-3 rounded-lg border border-error/20">{errors.submit}</p>}

          <div className="pt-8 flex flex-col sm:flex-row items-center justify-center gap-4 w-full">
            <button 
              type="submit" 
              disabled={loading || sendingResults}
              className="group relative flex items-center justify-center gap-2 bg-primary-container text-on-primary-container font-headline-sm text-headline-sm px-8 py-4 rounded-full shadow-glow hover:-translate-y-1 transition-all duration-300 uppercase disabled:opacity-50 w-full sm:w-auto"
            >
              {loading ? <Loader2 className="w-6 h-6 animate-spin" /> : (
                <>Confirm My Booking</>
              )}
            </button>
            <button
              type="button"
              onClick={handleSendResultsOnly}
              disabled={loading || sendingResults}
              className="group relative flex items-center justify-center gap-2 bg-surface-container-high border border-outline-variant text-on-surface font-headline-sm text-headline-sm px-8 py-4 rounded-full hover:bg-surface-container-highest hover:-translate-y-1 transition-all duration-300 uppercase disabled:opacity-50 w-full sm:w-auto"
            >
              {sendingResults ? <Loader2 className="w-6 h-6 animate-spin" /> : (
                <>Send me results instead</>
              )}
            </button>
          </div>
        </form>
      </div>

      <div className="absolute inset-0 -z-10 w-full h-full pointer-events-none overflow-hidden flex items-center justify-center opacity-20">
        <div className="w-[800px] h-[800px] bg-primary-container rounded-full blur-[120px] absolute -top-1/4 -right-1/4 mix-blend-screen opacity-20"></div>
      </div>
    </div>
  );
}
