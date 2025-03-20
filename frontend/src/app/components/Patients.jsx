'use client';
import { useState, useEffect } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function Patients() {
  const [patients, setPatients] = useState([]);
  const [displayCount, setDisplayCount] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/patients`);
        const data = await response.json();
        setPatients(data);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching patients:', error);
        setIsLoading(false);
      }
    };

    fetchPatients();
  }, []);

  const filteredPatients = patients?.filter((patient) =>
    Object.values(patient).some((value) =>
      String(value).toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  const displayedPatients = filteredPatients.slice(0, displayCount);

  if (isLoading) {
    return <div className="flex justify-center p-8">Loading...</div>;
  }

  return (
    <div className="container mx-auto p-6 space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Patients List</h1>
        <Input
          type="search"
          placeholder="Search patients..."
          className="max-w-xs"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Age</TableHead>
              <TableHead>Gender</TableHead>
              <TableHead>Phone</TableHead>
              <TableHead>Email</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {displayedPatients.map((patient) => (
              <TableRow key={patient.id}>
                <TableCell>{patient.id}</TableCell>
                <TableCell>{patient.name}</TableCell>
                <TableCell>{patient.age}</TableCell>
                <TableCell>{patient.gender}</TableCell>
                <TableCell>{patient.phone}</TableCell>
                <TableCell>{patient.email}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      {filteredPatients.length > displayCount && (
        <div className="flex justify-center mt-4">
          <Button
            onClick={() => setDisplayCount((prev) => Math.min(prev + 10, 1000))}
            variant="outline"
          >
            Show More
          </Button>
        </div>
      )}

      <div className="text-sm text-gray-500 text-center">
        Showing {displayedPatients.length} of {filteredPatients.length} entries
      </div>
    </div>
  );
}
