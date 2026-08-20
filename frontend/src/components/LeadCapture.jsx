import React, { useState } from 'react';
import { Loader2 } from 'lucide-react';
import Result from './Result';

export default function LeadCapture({ answers, campaignSource }) {
  const [formData, setFormData] = useState({ name: '', email: '', phone: '+91 ', bot_field: '' });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({ name: '', email: '', phone: '', submit: '' });
  const [resultData, setResultData] = useState(null);

  const validateFrontend = () => {
    let isValid = true;
    let newErrors = { name: '', email: '', phone: '', submit: '' };

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

    // Email Validation
    const emailVal = formData.email.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailVal)) {
      newErrors.email = 'Please provide a valid email address.';
      isValid = false;
    } else {
      const lowerEmail = emailVal.toLowerCase();
      const dummyDomains = ['test.com', 'example.com', 'dummy.com', 'a.com'];
      const domain = lowerEmail.split('@')[1];
      if (dummyDomains.includes(domain) || ['test@test.com', 'example@example.com'].includes(lowerEmail)) {
        newErrors.email = 'Please provide a valid email address.';
        isValid = false;
      }
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

  const handleEmailChange = (e) => {
    setFormData({ ...formData, email: e.target.value });
    if (errors.email) setErrors({ ...errors, email: '' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Bot prevention (Honeypot)
    if (formData.bot_field) {
      // Silently fail if bot field is filled
      setResultData({ title: "Bot detected", content: "Submission ignored." });
      return;
    }

    if (!validateFrontend()) return;

    setLoading(true);
    setErrors({ ...errors, submit: '' });

    const payload = {
      campaign_source: campaignSource,
      name: formData.name.trim(),
      email: formData.email.trim(),
      phone: formData.phone,
      assessment_answers: answers
    };

    try {
      // In production, this would point to the deployed FastAPI URL
      const response = await fetch(`${import.meta.env.VITE_API_URL || ''}/api/lead`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        if (response.status === 429) {
          throw new Error('Too many requests. Please try again later.');
        }
        throw new Error('Failed to submit assessment. Please try again.');
      }

      const data = await response.json();
      setResultData(data);
    } catch (err) {
      setErrors({ ...errors, submit: err.message || 'Something went wrong, please try again later.' });
    } finally {
      setLoading(false);
    }
  };

  if (resultData && resultData.title === "Bot detected") {
      return (
        <div className="flex-grow flex flex-col items-center justify-center p-8">
            <h2 className="text-xl font-bold">Submission ignored.</h2>
        </div>
      );
  }

  if (resultData) {
    return <Result data={resultData} />;
  }

  return (
    <div className="flex-grow flex flex-col items-center justify-center px-container-padding-mobile md:px-container-padding-desktop py-stack-lg relative w-full">
      <section className="w-full max-w-[500px] flex flex-col items-center relative z-10 slide-up-enter-active">
        <div className="w-full bg-surface-container rounded-xl p-stack-md md:p-stack-lg shadow-ambient border border-primary-container/30 relative">
          
          <h2 className="font-headline-md text-headline-md text-on-surface mb-2 text-center text-primary-container">
            Your Results Are Ready
          </h2>
          <p className="font-body-md text-body-md text-on-surface-variant text-center mb-stack-md">
            Enter your details below to reveal your personalized learning profile and timeline.
          </p>

          <form onSubmit={handleSubmit} className="flex flex-col gap-4" noValidate>
            
            {/* Honeypot field - visually hidden, screen readers ignore it ideally, or tell users to ignore */}
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

            <div>
              <label htmlFor="name" className="block font-label-caps text-label-caps text-on-surface-variant mb-2">Name <span className="text-error">*</span></label>
              <input 
                type="text" 
                id="name"
                required 
                className={`w-full bg-surface border ${errors.name ? 'border-error focus:border-error focus:ring-error' : 'border-surface-variant focus:border-primary-container focus:ring-primary-container'} rounded-lg p-3 text-on-surface focus:ring-1 outline-none transition-colors`}
                value={formData.name}
                onChange={handleNameChange}
                aria-invalid={!!errors.name}
                aria-describedby={errors.name ? "name-error" : undefined}
              />
              {errors.name && <p id="name-error" className="text-error text-sm mt-1">{errors.name}</p>}
            </div>
            
            <div>
              <label htmlFor="email" className="block font-label-caps text-label-caps text-on-surface-variant mb-2">Email <span className="text-error">*</span></label>
              <input 
                type="email" 
                id="email"
                required 
                className={`w-full bg-surface border ${errors.email ? 'border-error focus:border-error focus:ring-error' : 'border-surface-variant focus:border-primary-container focus:ring-primary-container'} rounded-lg p-3 text-on-surface focus:ring-1 outline-none transition-colors`}
                value={formData.email}
                onChange={handleEmailChange}
                aria-invalid={!!errors.email}
                aria-describedby={errors.email ? "email-error" : undefined}
              />
              {errors.email && <p id="email-error" className="text-error text-sm mt-1">{errors.email}</p>}
            </div>

            <div>
              <label htmlFor="phone" className="block font-label-caps text-label-caps text-on-surface-variant mb-2">Phone Number <span className="text-error">*</span></label>
              <input 
                type="tel" 
                id="phone"
                required 
                className={`w-full bg-surface border ${errors.phone ? 'border-error focus:border-error focus:ring-error' : 'border-surface-variant focus:border-primary-container focus:ring-primary-container'} rounded-lg p-3 text-on-surface focus:ring-1 outline-none transition-colors`}
                value={formData.phone}
                onChange={handlePhoneChange}
                placeholder="+91 "
                aria-invalid={!!errors.phone}
                aria-describedby={errors.phone ? "phone-error" : undefined}
              />
              {errors.phone && <p id="phone-error" className="text-error text-sm mt-1">{errors.phone}</p>}
            </div>

            {errors.submit && <p className="text-error text-sm text-center font-medium bg-error/10 p-2 rounded">{errors.submit}</p>}

            <button 
              type="submit" 
              disabled={loading}
              className="mt-4 w-full px-8 py-4 bg-primary-container text-on-primary-container rounded-full font-label-caps text-label-caps shadow-ambient hover:-translate-y-1 hover:shadow-glow transition-all duration-300 active:scale-95 flex items-center justify-center gap-2 uppercase disabled:opacity-50"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Reveal My Profile'}
            </button>
            <p className="text-center text-xs text-on-surface-variant mt-2 opacity-70">
              We respect your privacy. No spam.
            </p>
          </form>

        </div>
      </section>

      {/* Atmospheric background */}
      <div className="absolute inset-0 -z-10 w-full h-full pointer-events-none overflow-hidden flex items-center justify-center opacity-20">
        <div className="w-[800px] h-[800px] bg-primary-container rounded-full blur-[120px] absolute -top-1/4 -right-1/4 mix-blend-screen opacity-30"></div>
      </div>
    </div>
  );
}
