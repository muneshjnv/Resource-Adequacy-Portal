import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { throwError, BehaviorSubject, Observable } from 'rxjs';
import {catchError, map, mergeMap} from 'rxjs/operators'
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { JwtHelperService } from '@auth0/angular-jwt';
import swal from 'sweetalert2';
import { api_url } from '../helpers/urlentry';
import { ToastService } from 'src/app/account/login/toast-service';


@Injectable({
  providedIn: 'root'
})





export class AuthenticationService {
  

  url = api_url;
  constructor(public http: HttpClient, public toastService: ToastService ) {
    this.currentUserSubject = new BehaviorSubject<any>(JSON.parse(localStorage.getItem('currentUser')!));
        this.currentUser = this.currentUserSubject.asObservable();
   }

    // Handle authentication errors
    private currentUserSubject: BehaviorSubject<any>;
    public currentUser: Observable<any>;  

    login(username: string, password: string, captchaToken: string, device_id: string) {
      const deviceId = localStorage.getItem('device_id') || this.getDeviceId();
      localStorage.setItem('device_id', deviceId); // Store the generated Device ID
      const headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Device-ID': device_id // Include device_id in headers
      });
      return this.http.post<any>(`${this.url}/login`, { username, password, recaptcha: captchaToken }, { headers })
        .pipe(
          map(user => {
            if ('error' in user) {
              // Show error toast and refresh CAPTCHA
              this.toastService.show(user['error'], { classname: 'bg-danger text-white', delay: 5000 });
              this.refreshCaptcha();
            } else {
              // Store the entire user object directly (contains session_token, token, etc.)
              localStorage.setItem('currentUser', JSON.stringify(user));
    
              // Update the current user observable
              this.currentUserSubject.next(user);
    
              return user;
            }
          }),
          // catchError(this.handleError) // Add error handling if required
        );
    }

    refreshCaptcha() {
      // Assuming you're using Google reCAPTCHA v2 or v3
      if (window.grecaptcha) {
        window.grecaptcha.reset();  // For reCAPTCHA v2
        // For reCAPTCHA v3, you would re-execute it to get a new token:
        // grecaptcha.execute('your-site-key', { action: 'login' }).then(function(token) {
        //   this.captchaToken = token;
        // });
      }
    }

  public get currentUserValue(): any {
    return this.currentUserSubject.value;
}

generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

getDeviceId() {
  // Check if a Device ID already exists in localStorage
  let deviceId = localStorage.getItem('device_id');
  if (!deviceId) {
    // Generate a new Device ID and store it
    deviceId = this.generateUUID();
    localStorage.setItem('device_id', deviceId);
  }
  return deviceId;
}

  logout() {
      // remove user from local storage to log user out
      localStorage.removeItem('currentUser');
      this.currentUserSubject.next(null);
      // this.currentUserSubject = null;
  }

  isLoggedIn() {
    return this.http.get<any>(this.url + '/protected')
  }


}




