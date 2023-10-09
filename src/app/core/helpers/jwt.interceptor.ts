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
      // add auth header with jwt if user is logged in and request is to the api url
      // const currentUser = this.auth.currentUserValue;
      const currentUser = JSON.parse(localStorage.getItem('currentUser')!)
    //   const isLoggedIn = currentUser && currentUser.token;
    //   console.log("Sharingan");
    //   console.log(currentUser);
    //   console.log('Rinnegan')
      const isApiUrl = request.url.startsWith(this.url);

    //   console.log(isLoggedIn);
    //   console.log(isApiUrl);
      // console.log(currentUser);

      if(currentUser) {
        if (Object.keys(currentUser).length != 0 && isApiUrl) {
            request = request.clone({
                setHeaders: {
                    Authorization: `Bearer ${currentUser.token}`
                   
                    
                }
            });
        }  
      }
      
      return next.handle(request);
  }

   
}