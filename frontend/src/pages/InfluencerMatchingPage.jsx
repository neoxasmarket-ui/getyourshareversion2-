/**
 * Influencer Matching Page - Tinder for Business
 * Interface swipe pour trouver les meilleurs influenceurs
 * - Cartes swipables
 * - Score de match
 * - Détails influenceur
 * - Actions: Like, Dislike, Super Like
 */
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

// Icons
const HeartIcon = () => <span className="text-red-500">❤️</span>;
const CrossIcon = () => <span className="text-gray-500">✕</span>;
const StarIcon = () => <span className="text-yellow-500">⭐</span>;
const FireIcon = () => <span className="text-orange-500">🔥</span>;
const CheckIcon = () => <span className="text-green-500">✓</span>;

const InfluencerMatchingPage = () => {
  const { campaignId } = useParams();

  const [matches, setMatches] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [showMatchModal, setShowMatchModal] = useState(false);
  const [matchedInfluencer, setMatchedInfluencer] = useState(null);
  const [swipeDirection, setSwipeDirection] = useState(null);

  const cardRef = useRef(null);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);

  useEffect(() => {
    fetchMatches();
  }, [campaignId]);

  const fetchMatches = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get(`/api/matching/campaign/${campaignId}`);
      setMatches(response.data);
    } catch (error) {
      console.error('Erreur chargement matches:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const currentInfluencer = matches[currentIndex];

  // ============================================
  // DRAG & SWIPE HANDLERS
  // ============================================

  const handleDragStart = (e) => {
    const clientX = e.type === 'mousedown' ? e.clientX : e.touches[0].clientX;
    const clientY = e.type === 'mousedown' ? e.clientY : e.touches[0].clientY;

    setDragStart({ x: clientX, y: clientY });
    setIsDragging(true);
  };

  const handleDragMove = (e) => {
    if (!isDragging) return;

    const clientX = e.type === 'mousemove' ? e.clientX : e.touches[0].clientX;
    const clientY = e.type === 'mousemove' ? e.clientY : e.touches[0].clientY;

    const offsetX = clientX - dragStart.x;
    const offsetY = clientY - dragStart.y;

    setDragOffset({ x: offsetX, y: offsetY });

    // Déterminer direction
    if (Math.abs(offsetX) > 50) {
      setSwipeDirection(offsetX > 0 ? 'right' : 'left');
    } else {
      setSwipeDirection(null);
    }
  };

  const handleDragEnd = () => {
    setIsDragging(false);

    const threshold = 150; // Distance minimum pour swipe

    if (Math.abs(dragOffset.x) > threshold) {
      // Swipe validé
      if (dragOffset.x > 0) {
        handleSwipeRight();
      } else {
        handleSwipeLeft();
      }
    } else {
      // Reset position
      setDragOffset({ x: 0, y: 0 });
      setSwipeDirection(null);
    }
  };

  // ============================================
  // SWIPE ACTIONS
  // ============================================

  const handleSwipeRight = async () => {
    if (!currentInfluencer) return;

    // Animation sortie
    setDragOffset({ x: 1000, y: 0 });

    try {
      const response = await axios.post(`/api/matching/swipe-right`, {
        campaign_id: campaignId,
        influencer_id: currentInfluencer.influencer.id
      });

      if (response.data.match) {
        // C'est un MATCH!
        setMatchedInfluencer(currentInfluencer);
        setShowMatchModal(true);
      }

      // Passer au suivant après animation
      setTimeout(() => {
        nextInfluencer();
      }, 300);
    } catch (error) {
      console.error('Erreur swipe right:', error);
      nextInfluencer();
    }
  };

  const handleSwipeLeft = async () => {
    if (!currentInfluencer) return;

    // Animation sortie
    setDragOffset({ x: -1000, y: 0 });

    try {
      await axios.post(`/api/matching/swipe-left`, {
        campaign_id: campaignId,
        influencer_id: currentInfluencer.influencer.id
      });

      // Passer au suivant
      setTimeout(() => {
        nextInfluencer();
      }, 300);
    } catch (error) {
      console.error('Erreur swipe left:', error);
      nextInfluencer();
    }
  };

  const handleSuperLike = async () => {
    if (!currentInfluencer) return;

    // Animation spéciale
    setDragOffset({ x: 0, y: -1000 });

    try {
      await axios.post(`/api/matching/super-like`, {
        campaign_id: campaignId,
        influencer_id: currentInfluencer.influencer.id,
        premium_offer: {
          bonus: 500,
          priority: true
        }
      });

      setTimeout(() => {
        nextInfluencer();
      }, 300);
    } catch (error) {
      console.error('Erreur super like:', error);
      nextInfluencer();
    }
  };

  const nextInfluencer = () => {
    setDragOffset({ x: 0, y: 0 });
    setSwipeDirection(null);
    setCurrentIndex(prev => prev + 1);
  };

  // ============================================
  // RENDER
  // ============================================

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-indigo-500 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600">Recherche des meilleurs influenceurs...</p>
        </div>
      </div>
    );
  }

  if (currentIndex >= matches.length) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="text-6xl mb-4">🎉</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Tous les influenceurs vus!
          </h2>
          <p className="text-gray-600 mb-4">
            Consultez vos matches en attente de réponse
          </p>
          <button
            onClick={() => window.location.href = '/campaigns'}
            className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            Voir mes campagnes
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="influencer-matching-page min-h-screen bg-gradient-to-br from-pink-50 to-purple-50 p-6">
      {/* Header */}
      <div className="max-w-md mx-auto mb-6">
        <h1 className="text-2xl font-bold text-gray-900 text-center">
          Trouvez votre influenceur parfait
        </h1>
        <p className="text-gray-600 text-center mt-1">
          {matches.length - currentIndex} influenceurs restants
        </p>
      </div>

      {/* Swipe Cards Container */}
      <div className="max-w-md mx-auto relative" style={{ height: '600px' }}>
        {/* Background cards (stack effect) */}
        {matches.slice(currentIndex + 1, currentIndex + 3).map((match, idx) => (
          <div
            key={match.influencer.id}
            className="absolute top-0 left-0 right-0 bg-white rounded-2xl shadow-lg"
            style={{
              transform: `scale(${1 - (idx + 1) * 0.05}) translateY(${(idx + 1) * 10}px)`,
              zIndex: 10 - idx,
              opacity: 1 - (idx + 1) * 0.3
            }}
          >
            <div style={{ height: '600px' }}></div>
          </div>
        ))}

        {/* Current card */}
        {currentInfluencer && (
          <div
            ref={cardRef}
            className="absolute top-0 left-0 right-0 bg-white rounded-2xl shadow-2xl overflow-hidden cursor-grab active:cursor-grabbing"
            style={{
              transform: `translate(${dragOffset.x}px, ${dragOffset.y}px) rotate(${dragOffset.x / 20}deg)`,
              transition: isDragging ? 'none' : 'transform 0.3s ease-out',
              zIndex: 20
            }}
            onMouseDown={handleDragStart}
            onMouseMove={handleDragMove}
            onMouseUp={handleDragEnd}
            onMouseLeave={handleDragEnd}
            onTouchStart={handleDragStart}
            onTouchMove={handleDragMove}
            onTouchEnd={handleDragEnd}
          >
            {/* Swipe indicators */}
            {swipeDirection === 'right' && (
              <div className="absolute top-8 left-8 z-30 px-4 py-2 bg-green-500 text-white font-bold text-2xl rounded-lg transform rotate-12 border-4 border-green-600">
                LIKE
              </div>
            )}
            {swipeDirection === 'left' && (
              <div className="absolute top-8 right-8 z-30 px-4 py-2 bg-red-500 text-white font-bold text-2xl rounded-lg transform -rotate-12 border-4 border-red-600">
                NOPE
              </div>
            )}

            <InfluencerCard influencer={currentInfluencer} />
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="max-w-md mx-auto mt-6">
        <div className="flex items-center justify-center gap-6">
          {/* Dislike */}
          <button
            onClick={handleSwipeLeft}
            className="w-16 h-16 bg-white rounded-full shadow-lg flex items-center justify-center hover:scale-110 transition-transform"
          >
            <CrossIcon className="text-3xl" />
          </button>

          {/* Super Like */}
          <button
            onClick={handleSuperLike}
            className="w-16 h-16 bg-gradient-to-r from-blue-400 to-blue-600 rounded-full shadow-lg flex items-center justify-center hover:scale-110 transition-transform"
          >
            <StarIcon className="text-3xl" />
          </button>

          {/* Like */}
          <button
            onClick={handleSwipeRight}
            className="w-16 h-16 bg-gradient-to-r from-pink-400 to-red-500 rounded-full shadow-lg flex items-center justify-center hover:scale-110 transition-transform"
          >
            <HeartIcon className="text-3xl" />
          </button>
        </div>

        <div className="text-center mt-4 text-sm text-gray-600">
          Swipe ou utilisez les boutons
        </div>
      </div>

      {/* Match Modal */}
      {showMatchModal && matchedInfluencer && (
        <MatchModal
          influencer={matchedInfluencer}
          onClose={() => setShowMatchModal(false)}
        />
      )}
    </div>
  );
};

// ============================================
// INFLUENCER CARD COMPONENT
// ============================================

const InfluencerCard = ({ influencer }) => {
  const { influencer: inf, match_score, score_breakdown, estimated_reach, pricing, match_reasons } = influencer;

  return (
    <div className="h-full flex flex-col">
      {/* Image */}
      <div className="relative h-80 bg-gradient-to-br from-purple-400 to-pink-400">
        {inf.profile_picture ? (
          <img
            src={inf.profile_picture}
            alt={inf.name}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-white text-6xl">
            👤
          </div>
        )}

        {/* Match Score Badge */}
        <div className="absolute top-4 right-4 px-4 py-2 bg-white rounded-full shadow-lg">
          <div className="text-2xl font-bold text-indigo-600">{match_score}%</div>
          <div className="text-xs text-gray-600">Match</div>
        </div>

        {/* Tier Badge */}
        <div className="absolute bottom-4 left-4 px-3 py-1 bg-gradient-to-r from-yellow-400 to-orange-500 text-white font-bold rounded-full">
          {inf.tier || 'GOLD'}
        </div>
      </div>

      {/* Info */}
      <div className="flex-1 p-6 overflow-y-auto">
        {/* Name & Stats */}
        <div className="mb-4">
          <h3 className="text-2xl font-bold text-gray-900">{inf.name}</h3>
          <p className="text-gray-600">{inf.niche || 'Influenceur'}</p>

          <div className="flex items-center gap-4 mt-3 text-sm">
            <div className="flex items-center gap-1">
              <span className="font-semibold">{(inf.total_followers || 0).toLocaleString()}</span>
              <span className="text-gray-600">followers</span>
            </div>
            <div className="flex items-center gap-1">
              <span className="font-semibold">{inf.engagement_rate || 0}%</span>
              <span className="text-gray-600">engagement</span>
            </div>
          </div>
        </div>

        {/* Match Reasons */}
        <div className="mb-4">
          <h4 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
            <FireIcon /> Pourquoi ce match?
          </h4>
          <ul className="space-y-1">
            {(match_reasons || []).map((reason, idx) => (
              <li key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                <CheckIcon className="mt-0.5 flex-shrink-0" />
                <span>{reason}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Score Breakdown */}
        <div className="mb-4">
          <h4 className="font-semibold text-gray-900 mb-2">Score détaillé</h4>
          <div className="space-y-2">
            {Object.entries(score_breakdown || {}).map(([key, value]) => (
              <div key={key}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-600 capitalize">{key.replace('_', ' ')}</span>
                  <span className="font-semibold">{value}%</span>
                </div>
                <div className="bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-indigo-500 rounded-full h-2"
                    style={{ width: `${value}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Estimations */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          <div className="bg-blue-50 rounded-lg p-3">
            <div className="text-xs text-blue-600 mb-1">Portée estimée</div>
            <div className="text-lg font-bold text-blue-900">
              {(estimated_reach?.expected || 0).toLocaleString()}
            </div>
          </div>
          <div className="bg-green-50 rounded-lg p-3">
            <div className="text-xs text-green-600 mb-1">Prix</div>
            <div className="text-lg font-bold text-green-900">
              {(pricing?.recommended_price || 0).toLocaleString()} MAD
            </div>
          </div>
        </div>

        {/* Bio */}
        {inf.bio && (
          <div>
            <h4 className="font-semibold text-gray-900 mb-2">Bio</h4>
            <p className="text-sm text-gray-700">{inf.bio}</p>
          </div>
        )}
      </div>
    </div>
  );
};

// ============================================
// MATCH MODAL
// ============================================

const MatchModal = ({ influencer, onClose }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 animate-fadeIn">
      <div className="bg-white rounded-2xl p-8 max-w-md mx-4 text-center animate-scaleIn">
        <div className="text-6xl mb-4">💝</div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          C'EST UN MATCH!
        </h2>
        <p className="text-gray-600 mb-6">
          {influencer.influencer.name} est aussi intéressé par votre campagne!
        </p>

        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 px-6 py-3 border-2 border-gray-300 rounded-lg font-semibold hover:bg-gray-50"
          >
            Continuer
          </button>
          <button
            onClick={() => window.location.href = `/chat/${influencer.influencer.id}`}
            className="flex-1 px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-lg font-semibold hover:opacity-90"
          >
            Envoyer un message
          </button>
        </div>
      </div>
    </div>
  );
};

export default InfluencerMatchingPage;
