import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

/**
 * Interceptor que:
 * 1. Adiciona o token JWT automaticamente em todas as requisições
 * 2. Valida se o token está expirado antes de enviar
 * 3. Trata erros 401 (Unauthorized) limpando token e redirecionando para login
 */
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  const token = authService.getToken();
  
  if (token && authService.isTokenValid()) {
    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  } else if (token && !authService.isTokenValid()) {
    router.navigate(['/auth/login']);
  }
  
  return next(req).pipe(
    catchError((error) => {
  
      if (error.status === 401) {
        console.warn('🔒 Erro 401: Token rejeitado pelo servidor. Redirecionando para login...');
        
        authService.removeToken();
        
        router.navigate(['/auth/login']);
      }
      
      return throwError(() => error);
    })
  );
};

