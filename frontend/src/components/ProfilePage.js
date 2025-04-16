import React, { useState, useEffect } from 'react';
import ProfileHeader from './ProfileHeader';
import InterestTags from './InterestTags';

export default function ProfilePage() {
  const [userData, setUserData] = useState(null);


  if (!userData) return <div>Loading...</div>;

  return (
    <div className={styles.profileContainer}>
      <ProfileHeader user={userData} />
      <PhotoGallery photos={userData.photos} />
      
      <section className={styles.section}>
        <h2>About Me</h2>
        <p>{userData.bio || "This user hasn't written a bio yet"}</p>
      </section>

      <section className={styles.section}>
        <h2>Interests</h2>
        <InterestTags tags={userData.interests} />
      </section>

      <section className={styles.section}>
        <h2>Study Preferences</h2>
        <div className={styles.studyPrefs}>
          <p>Current Courses: {userData.studyPreferences.courses.join(', ')}</p>
          <p>Availability: {userData.studyPreferences.availability}</p>
        </div>
      </section>
    </div>
  );
};
