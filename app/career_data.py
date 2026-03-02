"""
Career Paths Database for Entertainment Industry

This module contains career path information used for matching
users to appropriate careers based on their interests, skills, and preferences.
"""

from typing import Dict, List


def get_career_paths() -> Dict[str, Dict]:
    """
    Return entertainment career paths database
    
    Returns:
        Dictionary of career paths with detailed information
    """
    return {
        "audio_engineer": {
            "name": "Audio Engineer",
            "description": "Record, mix, and master audio in studios or live settings. Work with artists, producers, and technical equipment to create high-quality sound.",
            "skills": ["technical aptitude", "attention to detail", "music knowledge", "problem-solving", "audio software proficiency"],
            "work_style": ["technical", "independent", "studio-based", "deadline-driven", "hands-on"],
            "salary_range": "$40k-$120k",
            "education": "Audio engineering certificate, associate's or bachelor's degree in audio production recommended",
            "entry_path": "Start as assistant engineer, intern at studios, build portfolio with independent projects"
        },
        
        "music_producer": {
            "name": "Music Producer",
            "description": "Create and produce music tracks, work with artists to develop their sound, oversee recording sessions, and make creative decisions about arrangement and production.",
            "skills": ["creative", "technical", "collaboration", "music theory", "DAW proficiency", "arrangement"],
            "work_style": ["creative", "collaborative", "flexible hours", "project-based", "entrepreneurial"],
            "salary_range": "$35k-$150k+ (highly variable)",
            "education": "Music production courses, self-taught with strong portfolio, or music degree",
            "entry_path": "Start making beats independently, build online presence, network with artists, offer affordable production services"
        },
        
        "content_creator": {
            "name": "Content Creator / Influencer",
            "description": "Create engaging content for social media, YouTube, TikTok, or other digital platforms. Build an audience and monetize through sponsorships, ads, or products.",
            "skills": ["creative", "video editing", "communication", "marketing", "social media savvy", "storytelling"],
            "work_style": ["independent", "flexible", "online", "entrepreneurial", "self-motivated"],
            "salary_range": "$20k-$500k+ (extremely variable)",
            "education": "No formal education required, but digital media or marketing courses helpful",
            "entry_path": "Start creating content consistently, find your niche, engage with audience, learn platform algorithms"
        },
        
        "video_editor": {
            "name": "Video Editor / Post-Production Specialist",
            "description": "Edit video content for films, TV shows, YouTube, commercials, or social media. Shape stories through cutting, color correction, and effects.",
            "skills": ["technical", "creative", "storytelling", "software proficiency", "attention to detail", "pacing"],
            "work_style": ["independent", "deadline-driven", "detail-oriented", "project-based"],
            "salary_range": "$35k-$90k",
            "education": "Film school, self-taught with portfolio, or digital media degree",
            "entry_path": "Build portfolio with personal projects, offer services on Fiverr/Upwork, assist established editors"
        },
        
        "sound_designer": {
            "name": "Sound Designer",
            "description": "Create audio effects, soundscapes, and original sounds for films, games, theater, or other media. Combine technical skills with creative innovation.",
            "skills": ["creative", "technical", "audio software", "innovation", "collaboration", "field recording"],
            "work_style": ["creative", "technical", "project-based", "collaborative", "experimental"],
            "salary_range": "$45k-$100k",
            "education": "Audio production degree or sound design certificate",
            "entry_path": "Build sound library, create demo reel, work on indie films/games, network in industry"
        },
        
        "talent_manager": {
            "name": "Talent Manager / Entertainment Manager",
            "description": "Manage artists' careers, negotiate deals, book gigs, develop strategies, and guide artists toward their goals. Be the business brain behind creative talent.",
            "skills": ["business", "networking", "negotiation", "communication", "organization", "people skills"],
            "work_style": ["people-oriented", "business-minded", "fast-paced", "networking-focused", "entrepreneurial"],
            "salary_range": "$40k-$200k+ (often commission-based)",
            "education": "Business degree helpful but not required, entertainment industry knowledge essential",
            "entry_path": "Start at talent agency, manage local artists, build relationships, understand contracts"
        },
        
        "concert_promoter": {
            "name": "Concert Promoter / Event Producer",
            "description": "Organize and promote live entertainment events, concerts, and shows. Handle logistics, marketing, venue booking, and ticket sales.",
            "skills": ["organization", "marketing", "networking", "budget management", "multitasking", "sales"],
            "work_style": ["entrepreneurial", "people-oriented", "high-energy", "deadline-driven", "risk-taking"],
            "salary_range": "$35k-$100k+ (variable, event-dependent)",
            "education": "Event management or business degree helpful",
            "entry_path": "Volunteer at events, work at venues, start small local events, build network of artists and vendors"
        },
        
        "music_journalist": {
            "name": "Music Journalist / Critic",
            "description": "Write about music, interview artists, review albums and concerts, and cover the music industry for publications, blogs, or media outlets.",
            "skills": ["writing", "music knowledge", "communication", "research", "interviewing", "deadlines"],
            "work_style": ["independent", "creative", "flexible", "deadline-driven", "research-focused"],
            "salary_range": "$30k-$80k",
            "education": "Journalism or communications degree recommended",
            "entry_path": "Start music blog, pitch articles to publications, build portfolio, attend shows and network"
        },
        
        "broadcast_technician": {
            "name": "Broadcast Technician / Production Engineer",
            "description": "Operate equipment for TV, radio, or streaming broadcasts. Set up cameras, audio, lighting, and ensure technical quality of live or recorded content.",
            "skills": ["technical", "problem-solving", "attention to detail", "equipment operation", "quick thinking"],
            "work_style": ["technical", "shift-based", "team-oriented", "fast-paced", "hands-on"],
            "salary_range": "$35k-$75k",
            "education": "Broadcasting or communications degree, or technical certification",
            "entry_path": "Intern at TV/radio station, work at college station, learn equipment, get certified"
        },
        
        "lighting_designer": {
            "name": "Lighting Designer / Lighting Technician",
            "description": "Design and operate lighting for concerts, theater productions, events, or film/TV sets. Create visual atmosphere through lighting choices.",
            "skills": ["creative", "technical", "artistic vision", "collaboration", "equipment knowledge", "programming"],
            "work_style": ["creative", "technical", "project-based", "collaborative", "hands-on"],
            "salary_range": "$40k-$90k",
            "education": "Theater tech degree or lighting design courses",
            "entry_path": "Work on local theater productions, assist established designers, learn lighting boards and equipment"
        },
        
        "dj": {
            "name": "DJ / Club DJ / Radio DJ",
            "description": "Mix and play music for live audiences at clubs, events, or on radio/streaming platforms. Read crowds, create energy, and curate musical experiences.",
            "skills": ["music knowledge", "technical skills", "crowd reading", "beatmatching", "marketing", "performance"],
            "work_style": ["performance-based", "night/weekend work", "independent", "entrepreneurial", "social"],
            "salary_range": "$25k-$200k+ (highly variable)",
            "education": "No formal education required, DJ courses available",
            "entry_path": "Practice at home, play house parties, build online presence, network with promoters, start with small gigs"
        },
        
        "a_and_r": {
            "name": "A&R (Artists & Repertoire)",
            "description": "Scout and develop new talent for record labels. Find promising artists, guide their development, and connect them with producers and songwriters.",
            "skills": ["music knowledge", "networking", "talent spotting", "communication", "business sense", "trend awareness"],
            "work_style": ["networking-focused", "research-intensive", "collaborative", "travel-involved", "trend-watching"],
            "salary_range": "$45k-$120k",
            "education": "Music business degree helpful",
            "entry_path": "Work at record label, build network of artists, attend shows constantly, develop ear for talent"
        },
        
        "music_teacher": {
            "name": "Music Teacher / Instructor",
            "description": "Teach music theory, instruments, or production to students of various ages. Work in schools, private lessons, or online platforms.",
            "skills": ["teaching", "patience", "music knowledge", "communication", "organization", "instrument proficiency"],
            "work_style": ["structured", "people-oriented", "flexible schedule", "independent or institutional"],
            "salary_range": "$35k-$70k (varies by setting)",
            "education": "Music degree often required for schools, less formal for private teaching",
            "entry_path": "Get teaching certification (if school-based), start private lessons, build reputation, use online platforms"
        },
        
        "tour_manager": {
            "name": "Tour Manager / Road Manager",
            "description": "Coordinate all logistics for artists on tour including travel, accommodations, schedules, budgets, and problem-solving on the road.",
            "skills": ["organization", "problem-solving", "communication", "budget management", "flexibility", "people skills"],
            "work_style": ["travel-heavy", "unpredictable", "fast-paced", "multitasking", "hands-on"],
            "salary_range": "$40k-$100k",
            "education": "No specific degree required, event management helpful",
            "entry_path": "Work on small tours, assist established tour managers, start with local acts, build reputation"
        },
        
        "music_video_director": {
            "name": "Music Video Director",
            "description": "Direct and produce music videos for artists. Develop creative concepts, work with cinematographers, and bring artistic vision to life.",
            "skills": ["creative vision", "directing", "storytelling", "collaboration", "visual aesthetics", "technical knowledge"],
            "work_style": ["creative", "project-based", "collaborative", "deadline-driven", "entrepreneurial"],
            "salary_range": "$40k-$150k+ (project-dependent)",
            "education": "Film school or self-taught with strong portfolio",
            "entry_path": "Make videos for local artists, build portfolio, use affordable equipment, network with musicians"
        },
        
        "streaming_specialist": {
            "name": "Streaming Content Manager / Live Stream Producer",
            "description": "Manage live streaming content for platforms like Twitch, YouTube Live, or corporate streams. Handle technical setup, production, and audience engagement.",
            "skills": ["technical", "multitasking", "audience engagement", "problem-solving", "software proficiency", "creativity"],
            "work_style": ["tech-focused", "flexible hours", "online-based", "fast-paced", "independent or team"],
            "salary_range": "$35k-$80k",
            "education": "Digital media or broadcasting background helpful",
            "entry_path": "Start own stream, work for streamers, build technical skills, learn OBS and streaming software"
        },
        
        "songwriter": {
            "name": "Songwriter / Lyricist",
            "description": "Write songs for yourself or other artists. Create melodies, lyrics, and musical compositions. Work independently or collaborate with artists and producers.",
            "skills": ["creative writing", "music theory", "melody creation", "collaboration", "instrument proficiency", "storytelling"],
            "work_style": ["creative", "flexible", "independent or collaborative", "project-based", "introspective"],
            "salary_range": "$25k-$200k+ (royalty-based, highly variable)",
            "education": "No formal education required, music theory helpful",
            "entry_path": "Write constantly, co-write with others, pitch songs to artists, register with PROs, build catalog"
        },
        
        "podcast_producer": {
            "name": "Podcast Producer / Audio Producer",
            "description": "Produce podcasts from conception to publication. Handle recording, editing, sound design, and distribution. Work with hosts to create engaging audio content.",
            "skills": ["audio editing", "storytelling", "organization", "creativity", "technical skills", "communication"],
            "work_style": ["independent", "deadline-driven", "creative", "detail-oriented", "flexible"],
            "salary_range": "$35k-$85k",
            "education": "Audio production or journalism background helpful",
            "entry_path": "Start own podcast, learn editing software, offer production services, build portfolio"
        }
    }


def get_career_path_by_name(career_name: str) -> Dict:
    """
    Get a specific career path by name
    
    Args:
        career_name: The name of the career path
    
    Returns:
        Career path dictionary or None if not found
    """
    paths = get_career_paths()
    
    # Try exact match first
    for key, path in paths.items():
        if path["name"].lower() == career_name.lower():
            return path
    
    # Try partial match
    for key, path in paths.items():
        if career_name.lower() in path["name"].lower():
            return path
    
    return None


def get_career_paths_by_skill(skill: str) -> List[Dict]:
    """
    Get career paths that match a specific skill
    
    Args:
        skill: The skill to search for
    
    Returns:
        List of career paths that include this skill
    """
    paths = get_career_paths()
    matching_paths = []
    
    skill_lower = skill.lower()
    
    for key, path in paths.items():
        path_skills = [s.lower() for s in path.get("skills", [])]
        if any(skill_lower in ps for ps in path_skills):
            matching_paths.append(path)
    
    return matching_paths


def get_career_paths_by_work_style(work_style: str) -> List[Dict]:
    """
    Get career paths that match a work style preference
    
    Args:
        work_style: The work style to search for (e.g., "independent", "collaborative")
    
    Returns:
        List of career paths that match this work style
    """
    paths = get_career_paths()
    matching_paths = []
    
    work_style_lower = work_style.lower()
    
    for key, path in paths.items():
        path_styles = [s.lower() for s in path.get("work_style", [])]
        if any(work_style_lower in ps for ps in path_styles):
            matching_paths.append(path)
    
    return matching_paths


def get_all_skills() -> List[str]:
    """
    Get a list of all unique skills across all career paths
    
    Returns:
        Sorted list of unique skills
    """
    paths = get_career_paths()
    all_skills = set()
    
    for path in paths.values():
        all_skills.update(path.get("skills", []))
    
    return sorted(list(all_skills))


def get_all_work_styles() -> List[str]:
    """
    Get a list of all unique work styles across all career paths
    
    Returns:
        Sorted list of unique work styles
    """
    paths = get_career_paths()
    all_styles = set()
    
    for path in paths.values():
        all_styles.update(path.get("work_style", []))
    
    return sorted(list(all_styles))


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'get_career_paths',
    'get_career_path_by_name',
    'get_career_paths_by_skill',
    'get_career_paths_by_work_style',
    'get_all_skills',
    'get_all_work_styles',
]