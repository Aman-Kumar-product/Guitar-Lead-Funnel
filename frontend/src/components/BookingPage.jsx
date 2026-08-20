import React from 'react';
import { useSearchParams } from 'react-router-dom';
import BookingForm from './BookingForm';

export default function BookingPage() {
  const [searchParams] = useSearchParams();
  const lead_id = searchParams.get('lead_id');
  const email = searchParams.get('email');
  
  const [leadData, setLeadData] = React.useState(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    if (lead_id) {
      fetch(`${import.meta.env.VITE_API_URL || ''}/api/lead/${lead_id}`)
        .then(res => {
          if (!res.ok) throw new Error('Lead not found');
          return res.json();
        })
        .then(data => {
          setLeadData(data);
          setLoading(false);
        })
        .catch(err => {
          console.error(err);
          // Fallback if backend fails or lead isn't found
          setLeadData({
            lead_id,
            email,
            score_details: { is_qualified: true },
            booking_status: "Pending"
          });
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, [lead_id, email]);

  if (!lead_id || !email) {
    return (
      <div className="flex-grow flex flex-col items-center justify-center p-8 text-center text-on-surface">
        <h2 className="font-headline-md mb-2">Invalid Booking Link</h2>
        <p className="text-on-surface-variant">Please use the exact link provided in your email to book your strategy session.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex-grow flex flex-col items-center justify-center p-8">
        <p className="text-on-surface-variant font-label-caps uppercase animate-pulse">Loading booking details...</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-surface">
      <BookingForm leadData={leadData} fromEmail={true} />
    </div>
  );
}
