import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { Form } from '@angular/forms';

export interface ProfileData {
  username: string;
  email: string;
  favorite_music_genre: string;
  profile_picture: string | null;
}

export interface OtherProfileData {
  username: string;
  favorite_music_genre: string;
  profile_picture: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  
  constructor(
    private api: ApiService
  ) { }

 
  getProfile(username: string) {
    return this.api.get<ProfileData | OtherProfileData>(`user/${username}/profile`);
  }

  updateProfilePicture(pictureData:FormData) {
    return this.api.patch<null>('user/profile/change-picture', pictureData);
  }
}
