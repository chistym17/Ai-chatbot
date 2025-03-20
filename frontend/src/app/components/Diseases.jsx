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
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';

export default function Diseases() {
  const [diseases, setDiseases] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchDiseases = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/diseases`);
        const data = await response.json();
        setDiseases(data);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching diseases:', error);
        setIsLoading(false);
      }
    };

    fetchDiseases();
  }, []);

  const filteredDiseases = diseases?.filter((disease) =>
    Object.values(disease).some((value) =>
      String(value).toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  const truncateText = (text, maxLength = 100) => {
    if (text.length <= maxLength) return text;
    return text.slice(0, maxLength) + '...';
  };

  if (isLoading) {
    return <div className="flex justify-center p-8">Loading...</div>;
  }

  return (
    <div className="container mx-auto p-6 space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Diseases List</h1>
        <Input
          type="search"
          placeholder="Search diseases..."
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
              <TableHead className="w-1/4">Description</TableHead>
              <TableHead className="w-1/4">Symptoms</TableHead>
              <TableHead className="w-1/4">Common Treatments</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredDiseases.map((disease) => (
              <TableRow key={disease.id}>
                <TableCell>{disease.id}</TableCell>
                <TableCell>{disease.name}</TableCell>
                <TableCell>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger className="text-left">
                        {truncateText(disease.description)}
                      </TooltipTrigger>
                      <TooltipContent className="max-w-sm">
                        <p>{disease.description}</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </TableCell>
                <TableCell>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger className="text-left">
                        {truncateText(disease.symptoms)}
                      </TooltipTrigger>
                      <TooltipContent className="max-w-sm">
                        <p>{disease.symptoms}</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </TableCell>
                <TableCell>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger className="text-left">
                        {truncateText(disease.common_treatments)}
                      </TooltipTrigger>
                      <TooltipContent className="max-w-sm">
                        <p>{disease.common_treatments}</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <div className="text-sm text-gray-500 text-center">
        Total Diseases: {filteredDiseases.length}
      </div>
    </div>
  );
}
