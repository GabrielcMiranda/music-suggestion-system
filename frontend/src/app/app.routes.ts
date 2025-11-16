import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { guestGuard } from './core/guards/guest.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'music/recommendation',
    pathMatch: 'full'
  },
  {
    path: 'auth/login',
    loadComponent: () => import('./modules/auth/pages/login/login').then(m => m.Login),
    canActivate: [guestGuard]  
  },
  {
    path: 'auth/register',
    loadComponent: () => import('./modules/auth/pages/register/register').then(m => m.Register),
    canActivate: [guestGuard]  
  },
  {
    path: 'music/recommendation',
    loadComponent: () => import('./modules/music/pages/recommendation/recommendation').then(m => m.Recommendation),
    canActivate: [authGuard]  
  },
  {
    path: 'user/profile',
    loadComponent: () => import('./modules/user/pages/profile/profile').then(m => m.Profile),
    canActivate: [authGuard]
  }
];
