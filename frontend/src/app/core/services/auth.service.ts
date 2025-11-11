import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private tokenKey = 'access_token';
  
  constructor(private api: ApiService){}

  login(loginData: {login:string, password:string}){
    return this.api.post<{access_token:string, token_type:string}>('auth/login', loginData).pipe(
      tap(response => {
        localStorage.setItem(this.tokenKey, response.access_token);
      })
    );
  }

  register(registerData: {username:string, email:string, password:string}){
    return this.api.post<{access_token:string, token_type:string}>('auth/register', registerData).pipe(
      tap(response => {
        localStorage.setItem(this.tokenKey, response.access_token);
      })
    );
  }

  getToken(){
    return localStorage.getItem(this.tokenKey);
  }

  removeToken() {
    return localStorage.removeItem('access_token');
  }
  
}
