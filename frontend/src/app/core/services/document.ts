import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Document } from '../models/document.model';

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  private documentsSubject = new BehaviorSubject<Document[]>([]);
  documents$ = this.documentsSubject.asObservable();
  
  private selectedDocumentSubject = new BehaviorSubject<Document | null>(null);
  selectedDocument$ = this.selectedDocumentSubject.asObservable();
  
  private uploadProgressSubject = new BehaviorSubject<number>(0);
  uploadProgress$ = this.uploadProgressSubject.asObservable();

  constructor() {
    this.loadFromStorage();
  }

  // Add a document
  addDocument(document: Document): void {
    const current = this.documentsSubject.value;
    const exists = current.some(d => d.name === document.name);
    
    if (!exists) {
      const updated = [document, ...current];
      this.documentsSubject.next(updated);
      this.saveToStorage(updated);
      
      // Auto-select if first document
      if (current.length === 0) {
        this.selectDocument(document);
      }
    }
  }

  // Remove document
  removeDocument(documentName: string): void {
    const current = this.documentsSubject.value;
    const updated = current.filter(d => d.name !== documentName);
    this.documentsSubject.next(updated);
    this.saveToStorage(updated);
    
    // Clear selection if removed
    if (this.selectedDocumentSubject.value?.name === documentName) {
      this.selectedDocumentSubject.next(updated.length > 0 ? updated[0] : null);
    }
  }

  // Select document
  selectDocument(document: Document | null): void {
    this.selectedDocumentSubject.next(document);
  }

  // Update upload progress
  setUploadProgress(progress: number): void {
    this.uploadProgressSubject.next(progress);
  }

  // Reset upload progress
  resetUploadProgress(): void {
    this.uploadProgressSubject.next(0);
  }

  // Get document by name
  getDocumentByName(name: string): Document | undefined {
    return this.documentsSubject.value.find(d => d.name === name);
  }

  // Check if document exists
  hasDocument(name: string): boolean {
    return this.documentsSubject.value.some(d => d.name === name);
  }

  // Clear all documents
  clearAll(): void {
    this.documentsSubject.next([]);
    this.selectedDocumentSubject.next(null);
    localStorage.removeItem('documents');
  }

  // Save to localStorage
  private saveToStorage(documents: Document[]): void {
    localStorage.setItem('documents', JSON.stringify(documents));
  }

  // Load from localStorage
  private loadFromStorage(): void {
    const stored = localStorage.getItem('documents');
    if (stored) {
      const docs = JSON.parse(stored);
      this.documentsSubject.next(docs);
      if (docs.length > 0) {
        this.selectDocument(docs[0]);
      }
    }
  }
}