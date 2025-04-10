import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { api_url } from '../helpers/urlentry';

@Injectable({
  providedIn: 'root'
})
export class IntradayForecastService {

  url = api_url;

  constructor(private http: HttpClient) { }

  uploadIntradayFile(formData: any) {
    return this.http.post<any>(this.url + '/uploadintraday', formData)
  }

  fetchRevisions(state: any, date: any) {
    return this.http.post<any>(this.url + '/fetchintradayrevisions', {"state": state, "date": date})

  }

  fetchRevisionsData(state: any, date: any, revision: any) {
    return this.http.post<any>(this.url + '/fetchintradayrevisionsdata', {"state": state, "date": date, "revision": revision})
  }

  // fetchPendingEntry() {
  //   return this.http.get<any>(this.url + '/pendingentries')
  // }

  downloadIntradayReport(state: any, date: any, revision: any) {
    return this.http.post<any>(this.url + '/downloadintraday', {"state": state, "date": date, "revision": revision}, {
      responseType: 'blob' as 'json'  // This is necessary to handle Blob data correctly
    })
  }
}
