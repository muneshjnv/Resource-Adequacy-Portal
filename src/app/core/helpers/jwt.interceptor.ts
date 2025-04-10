import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor, HttpErrorResponse, HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { throwError } from 'rxjs';
import { retry, catchError, mergeMap } from 'rxjs/operators';
import { Router } from '@angular/router';
// import 'rxjs/add/operator/mergeMap';
// import 'rxjs/add/operator/catch';
// import { mergeMap, catchError } from 'rxjs/operators';
// import {_throw} from 'rxjs/add/operator/catch';
// import { ErrorObservable } from 'rxjs/observable/ErrorObservable';
import { AuthenticationService } from '../services/auth.service';
import { api_url } from './urlentry';


@Injectable()
export class JwtInterceptor implements HttpInterceptor {

    url = api_url;

    constructor(private router: Router, private http: HttpClient, public auth: AuthenticationService){}


    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
      // Get the current user from localStorage
      const currentUser = JSON.parse(localStorage.getItem('currentUser')!);
      
      const deviceId = localStorage.getItem('device_id') || this.getDeviceId();
      localStorage.setItem('device_id', deviceId); // Store the generated Device ID
      // Check if the user is logged in and the request is to the API URL
      const isApiUrl = request.url.startsWith(this.url);
  
      if (currentUser) {
          if (Object.keys(currentUser).length !== 0 && isApiUrl) {
              // Clone the request and add both JWT and Session Token headers
              request = request.clone({
                  setHeaders: {
                      Authorization: `Bearer ${currentUser.token}`,       // JWT token
                      'X-Session-Token': currentUser.session_token,        // Session token
                      'Device-ID': deviceId // Include device_id in headers
                    }
              });
          }
      }
      
      return next.handle(request);
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
  

   
}