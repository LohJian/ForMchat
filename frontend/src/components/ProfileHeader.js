import React from 'react';
import styles from '../styles/ProfilePage.module.css';
import { mockUser } from '../mockData';

function ProfileHeader({ user = mockUser }) {
    return(
        <div className={styles.header}>
            <img
                src={user.avatar}
                alt="Profile"
                className={styles.avatar}
            />
            <div className={styles.basicInfo}>
                <h1>{user.name},{user.age}</h1>
                <p>📍{user.location}</p>
            </div>
        </div>
    );

}
export default ProfileHeader