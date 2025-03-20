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
import { Input } from '@/components/ui/input';

export default function Hospitals() {
  const [hospitals, setHospitals] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchHospitals = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/hospitals`);
        const data = await response.json();
        setHospitals(data);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching hospitals:', error);
        setIsLoading(false);
      }
    };

    fetchHospitals();
  }, []);

  const filteredHospitals = hospitals?.filter((hospital) =>
    Object.values(hospital).some((value) =>
      String(value).toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  if (isLoading) {
    return <div className="flex justify-center p-8">Loading...</div>;
  }

  return (
    <div className="container mx-auto p-6 space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Hospitals List</h1>
        <Input
          type="search"
          placeholder="Search hospitals..."
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
              <TableHead>Location</TableHead>
              <TableHead>Contact</TableHead>
              <TableHead>Established Date</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredHospitals.map((hospital) => (
              <TableRow key={hospital.id}>
                <TableCell>{hospital.id}</TableCell>
                <TableCell>{hospital.name}</TableCell>
                <TableCell>{hospital.location}</TableCell>
                <TableCell>{hospital.contact}</TableCell>
                <TableCell>
                  {new Date(hospital.established_date).toLocaleDateString()}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <div className="text-sm text-gray-500 text-center">
        Total Hospitals: {filteredHospitals.length}
      </div>
    </div>
  );
}
